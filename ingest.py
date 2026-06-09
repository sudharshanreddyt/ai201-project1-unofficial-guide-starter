"""
ingest.py
---------
Public API for loading and chunking cleaned documents.

  load_documents()                   -> list[dict]
      Reads every .txt file from documents/cleaned/ and returns a list of
      { "doc_name": str, "text": str, "source_url": str } dicts.

  chunk_document(text, doc_name)     -> list[dict]
      Splits *text* into overlapping character-level chunks and returns a
      list of { "doc_name": str, "chunk_index": int, "text": str } dicts.

Chunk size and overlap are configured in config.py (CHUNK_SIZE, CHUNK_OVERLAP).
Document paths are configured in config.py (DOCS_PATH, CLEANED_SUBDIR).

To re-scrape and rebuild the cleaned files, run scraper.py directly:
    python scraper.py
"""

import logging
from pathlib import Path

import config

log = logging.getLogger(__name__)

# ── paths ─────────────────────────────────────────────────────────────────────
CLEAN_DIR = Path(config.DOCS_PATH) / config.CLEANED_SUBDIR


# ── public API ────────────────────────────────────────────────────────────────

def load_documents() -> list[dict]:
    """
    Read every .txt file in the cleaned documents directory.

    Returns a list of dicts, one per file:
        {
            "doc_name":   str,   # filename stem, e.g. "cs_jobs"
            "source_url": str,   # the SOURCE_URL line at the top of the file
            "text":       str,   # full document text (after the header line)
        }

    Files that cannot be read are skipped with a warning.
    """
    docs = []
    txt_files = sorted(CLEAN_DIR.glob("*.txt"))

    if not txt_files:
        log.warning("No .txt files found in %s. Run scraper.py first.", CLEAN_DIR)
        return docs

    for path in txt_files:
        try:
            raw = path.read_text(encoding="utf-8")
        except OSError as exc:
            log.warning("Could not read %s — %s", path.name, exc)
            continue

        # Extract SOURCE_URL from the first line, then the rest is content
        lines = raw.splitlines()
        source_url = ""
        content_start = 0

        if lines and lines[0].startswith("SOURCE_URL:"):
            source_url = lines[0].removeprefix("SOURCE_URL:").strip()
            # Skip the blank separator line after the header
            content_start = 2

        text = "\n".join(lines[content_start:]).strip()

        docs.append({
            "doc_name": path.stem,
            "source_url": source_url,
            "text": text,
        })

    log.info("Loaded %d document(s) from %s", len(docs), CLEAN_DIR)
    return docs


def chunk_document(text: str, doc_name: str) -> list[dict]:
    """
    Split *text* into overlapping character-level chunks.

    Chunk boundaries respect paragraph breaks where possible: the splitter
    first tries to break at the nearest double-newline within the window,
    so chunks stay semantically coherent.

    Parameters
    ----------
    text     : full document text
    doc_name : identifier carried into every chunk dict (e.g. "cs_jobs")

    Returns a list of dicts:
        {
            "doc_name":    str,   # same as *doc_name*
            "chunk_index": int,   # 0-based position within the document
            "text":        str,   # chunk content
        }

    Chunk size and overlap come from config.CHUNK_SIZE / config.CHUNK_OVERLAP.
    """
    size = config.CHUNK_SIZE
    overlap = config.CHUNK_OVERLAP

    if not text:
        return []

    chunks = []
    start = 0
    idx = 0

    while start < len(text):
        end = start + size

        # Try to snap the boundary to the nearest paragraph break (≤ 200 chars
        # before the hard cut) so we don't split mid-sentence.
        if end < len(text):
            snap = text.rfind("\n\n", start, end)
            if snap != -1 and snap > start:
                end = snap  # break at paragraph boundary

        chunk_text = text[start:end].strip()
        if chunk_text:
            chunks.append({
                "doc_name": doc_name,
                "chunk_index": idx,
                "text": chunk_text,
            })
            idx += 1

        # Advance by (size - overlap), but at least 1 to prevent infinite loop
        advance = max(size - overlap, 1)
        start += advance

    print(f"Chunked {doc_name} into {len(chunks)} chunks")
    return chunks

# print 5 chunks
if __name__ == "__main__":
    docs = load_documents()
    chunks = []
    for doc in docs:
        chunks.extend(chunk_document(doc["text"],doc["doc_name"]))
    print("\n----- Total ingested chunks:")
    print(f"{len(chunks)} chunks (from {len(docs)} documents)")

    sample_chunks = chunk_document(docs[0]["text"],docs[0]["doc_name"])
    print("\n----- Sample of 5 chunks:")
    for i, chunk in enumerate(sample_chunks[:5]):
        print(f"Chunk {i}: {chunk}")
    