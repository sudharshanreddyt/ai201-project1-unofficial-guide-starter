"""
retrieval.py
------------
Embedding, storage, and semantic retrieval against ChromaDB.

Public API
----------
  embed_and_store(chunks)   -- embed chunks and upsert into the vector DB
  retrieve(query)           -- semantic search, returns ranked result dicts
  get_collection()          -- direct handle to the ChromaDB collection

All settings (model, paths, collection name, result count) come from config.py.
"""

import logging

import chromadb
from chromadb.utils import embedding_functions

from config import CHROMA_COLLECTION, CHROMA_PATH, EMBEDDING_MODEL, N_RESULTS

log = logging.getLogger(__name__)

# ── ChromaDB setup (initialised once at module load) ─────────────────────────
# sentence-transformers downloads the model on first use — this may take
# 30-60 seconds the very first time. Subsequent runs use a local cache.
_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name=EMBEDDING_MODEL
)

_client = chromadb.PersistentClient(path=CHROMA_PATH)

_collection = _client.get_or_create_collection(
    name=CHROMA_COLLECTION,
    embedding_function=_ef,
    metadata={"hnsw:space": "cosine"},
)


def get_collection():
    """Return the ChromaDB collection (used by app.py during ingestion)."""
    return _collection


def embed_and_store(chunks: list[dict]) -> None:
    """
    Embed a list of chunk dicts and upsert them into the vector database.

    Each chunk must contain:
        "doc_name"    : str   -- document identifier (e.g. "cs_jobs")
        "chunk_index" : int   -- position within the document (0-based)
        "text"        : str   -- the chunk content to embed

    Optionally, chunks may also contain:
        "source_url"  : str   -- stored as metadata if present

    _collection.upsert() is used instead of .add() so that re-running
    ingestion never crashes with duplicate-ID errors — existing entries are
    simply overwritten with fresh embeddings.

    ChromaDB's embedding function (sentence-transformers) converts the raw
    text strings to vectors automatically — no manual embedding step needed.
    """
    if not chunks:
        log.warning("embed_and_store called with an empty chunk list — nothing stored.")
        return

    documents = [c["text"] for c in chunks]
    metadatas = [
        {
            "doc_name":  c["doc_name"],
            "doc_title": c.get("doc_title", ""),
            # source_url is optional — chunks from chunk_document() don't
            # include it, but callers that enrich chunks (e.g. app.py) may.
            "source_url": c.get("source_url", ""),
        }
        for c in chunks
    ]
    ids = [f"{c['doc_name']}_{c['chunk_index']}" for c in chunks]

    _collection.upsert(
        documents=documents,
        metadatas=metadatas,
        ids=ids,
    )
    log.info("embed_and_store: upserted %d chunks → collection now has %d total.",
             len(chunks), _collection.count())


def retrieve(query: str, n_results: int = N_RESULTS) -> list[dict]:
    """
    Semantic search: find the *n_results* most relevant chunks for *query*.

    Returns a list of dicts (sorted by relevance, best first):
        {
            "text"       : str    -- chunk content
            "doc_name"   : str    -- source document name
            "source_url" : str    -- original URL (empty string if not stored)
            "distance"   : float  -- cosine distance (lower = more similar)
        }

    Returns an empty list if the collection is empty or the query is blank.
    """
    if not query.strip():
        return []

    if _collection.count() == 0:
        log.warning("retrieve called but the collection is empty. Run embed_and_store first.")
        return []

    results = _collection.query(
        query_texts=[query],
        n_results=n_results,
        include=["documents", "metadatas", "distances"],
    )

    # _collection.query() returns nested lists — one list per query text.
    # We always pass a single query, so index [0] gives the actual results.
    docs  = results["documents"][0]
    metas = results["metadatas"][0]
    dists = results["distances"][0]

    chunks = []
    for doc, meta, dist in zip(docs, metas, dists):
        chunks.append({
            "text":       doc,
            "doc_name":   meta.get("doc_name", ""),
            "doc_title":  meta.get("doc_title", ""),
            "source_url": meta.get("source_url", ""),
            "distance":   dist,
        })
        log.debug("[%s] dist=%.3f  %s…", meta.get("doc_name"), dist, doc[:80])

    return chunks


if __name__ == "__main__":

    collection = get_collection()
    if collection.count() == 0:
        log.info("Collection is empty. Ingesting documents.")

        from ingest import load_documents, chunk_document

        # ── Step 1: ingest all documents ─────────────────────────────────────────
        docs = load_documents()
        all_chunks = []

        for doc in docs:
            doc_chunks = chunk_document(doc["text"], doc["doc_name"])
            # Enrich chunks with source_url and doc_title for metadata storage
            for ch in doc_chunks:
                ch["source_url"] = doc["source_url"]
                ch["doc_title"]  = doc.get("doc_title", "")
            all_chunks.extend(doc_chunks)

        log.info("Total chunks across %d documents: %d", len(docs), len(all_chunks))

        embed_and_store(all_chunks)

    # ── Step 2: test retrieval ────────────────────────────────────────────────
    test_queries = [
        "What do students say about the pacing and rigor of early computer science classes at GWU?",
        "Is the freshman housing lottery actually random, or does the placement matrix favor certain preferences?",
        "What are the best strategies for navigating the high-stress course registration process at GWU?",
    ]

    for query in test_queries:
        print(f"\n{'-'*60}")
        print(f"Query: {query}")
        print('-'*60)
        hits = retrieve(query)
        if not hits:
            print("  (no results)")
            continue
        for i, hit in enumerate(hits, 1):
            print(f"  {i}. [{hit['doc_name']}] dist={hit['distance']:.3f}")
            print(f"     {hit['text'].strip()}…")
            if hit["source_url"]:
                print(f"     {hit['source_url']}")
