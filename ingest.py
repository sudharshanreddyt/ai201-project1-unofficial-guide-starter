"""
ingest.py
---------
Public API for loading and chunking cleaned documents.

  load_documents()                   -> list[dict]
      Reads every .txt file from documents/cleaned/ and returns a list of
      {
          "doc_name":   str,   # filename stem, e.g. "cs_jobs"
          "source_url": str,   # the SOURCE_URL line at the top of the file
          "doc_title":  str,   # extracted from [POST TITLE] line
          "post_body":  str,   # the original Reddit post body (metadata only)
          "text":       str,   # comments/replies only — used for chunking
      } dicts.

  chunk_document(doc)                -> list[dict]
      Splits doc["text"] into overlapping character-level chunks and returns
      a list of dicts that carry all doc metadata plus the chunk text.

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
            "doc_title":  str,   # extracted from [POST TITLE] line (empty if none)
            "post_body":  str,   # the original Reddit post body (stored as metadata)
            "text":       str,   # comments/replies only — used for chunking
        }

    The post body (the original question/post content between [POST BODY] and
    the first comment) is extracted as metadata so it is available to the LLM
    for context but is NOT included in chunk text.  Chunking only operates on
    the community comments/replies, which contain the actual answers.

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

        lines = raw.splitlines()
        source_url = ""
        content_start = 0

        if lines and lines[0].startswith("SOURCE_URL:"):
            source_url = lines[0].removeprefix("SOURCE_URL:").strip()
            content_start = 2          # skip SOURCE_URL line + blank separator

        body_lines = lines[content_start:]

        # ── Parse structural sections ──────────────────────────────────────
        # Layout of a cleaned file (after SOURCE_URL header):
        #   [POST TITLE] <title text>
        #   (blank line)
        #   [POST BODY]
        #   <post body paragraphs…>
        #   (blank line)
        #   <comment 1>
        #   <comment 2>  …
        #
        # Strategy:
        #   1. Grab doc_title from the [POST TITLE] line.
        #   2. Collect lines between [POST BODY] and the first blank line
        #      after it as post_body (metadata — NOT chunked).
        #   3. Everything after the post body section becomes the chunk text
        #      (the community comments/replies).

        doc_title = ""
        post_body_lines: list[str] = []
        comment_lines:   list[str] = []

        IN_HEADER   = 0  # before [POST BODY]
        IN_BODY     = 1  # inside post body block
        IN_COMMENTS = 2  # after the first blank line following body

        state = IN_HEADER

        for line in body_lines:
            if state == IN_HEADER:
                if line.startswith("[POST TITLE]"):
                    doc_title = line.removeprefix("[POST TITLE]").strip()
                elif line.strip() == "[POST BODY]":
                    state = IN_BODY   # start collecting body text
                # else: skip blank / other header lines

            elif state == IN_BODY:
                if line.strip() == "" and not post_body_lines:
                    # blank line immediately after [POST BODY] label — ignore
                    continue
                if line.strip() == "" and post_body_lines:
                    # first blank line AFTER body content → switch to comments
                    state = IN_COMMENTS
                else:
                    post_body_lines.append(line)

            else:  # IN_COMMENTS
                comment_lines.append(line)

        post_body = "\n".join(post_body_lines).strip()
        text      = "\n".join(comment_lines).strip()

        docs.append({
            "doc_name":   path.stem,
            "source_url": source_url,
            "doc_title":  doc_title,
            "post_body":  post_body,
            "text":       text,
        })

    log.info("Loaded %d document(s) from %s", len(docs), CLEAN_DIR)
    return docs


def chunk_document(doc: dict) -> list[dict]:
    """
    Split the comments/replies in *doc* into overlapping character-level chunks.

    Chunk boundaries respect paragraph breaks where possible: the splitter
    first tries to break at the nearest double-newline within the window,
    so chunks stay semantically coherent.

    Parameters
    ----------
    doc : a document dict as returned by load_documents(), containing:
          - "text"       : comments/replies text to chunk
          - "doc_name"   : identifier (e.g. "cs_jobs")
          - "doc_title"  : post title
          - "source_url" : original Reddit URL
          - "post_body"  : original post body (stored as metadata, not chunked)

    Returns a list of dicts:
        {
            "doc_name":    str,   # e.g. "cs_jobs"
            "doc_title":   str,   # post title
            "source_url":  str,   # original Reddit URL
            "post_body":   str,   # original post body (metadata, not chunk text)
            "chunk_index": int,   # 0-based position within the document
            "text":        str,   # chunk content (comments/replies only)
        }

    Chunk size and overlap come from config.CHUNK_SIZE / config.CHUNK_OVERLAP.
    """
    size    = config.CHUNK_SIZE
    overlap = config.CHUNK_OVERLAP
    text    = doc.get("text", "")

    if not text:
        return []

    # Metadata to carry through to every chunk
    meta = {
        "doc_name":   doc.get("doc_name", ""),
        "doc_title":  doc.get("doc_title", ""),
        "source_url": doc.get("source_url", ""),
        "post_body":  doc.get("post_body", ""),
    }

    chunks = []
    start  = 0
    idx    = 0

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
                **meta,
                "chunk_index": idx,
                "text":        chunk_text,
            })
            idx += 1

        # Advance by (size - overlap), but at least 1 to prevent infinite loop
        advance = max(size - overlap, 1)
        start += advance

    print(f"Chunked {meta['doc_name']} into {len(chunks)} chunks")
    return chunks

# ── smoke-test ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    docs = load_documents()
    chunks = []
    for doc in docs:
        chunks.extend(chunk_document(doc))
    print("\n----- Total ingested chunks:")
    print(f"{len(chunks)} chunks (from {len(docs)} documents)")

    sample_chunks = chunk_document(docs[0])
    print("\n----- Sample of 5 chunks:")
    for i, chunk in enumerate(sample_chunks[:5]):
        print(f"Chunk {i}: {chunk}")

    print("\n----- Post body (metadata, not chunked):")
    print(f"  doc_name  : {docs[0]['doc_name']}")
    print(f"  post_body : {docs[0]['post_body']}")