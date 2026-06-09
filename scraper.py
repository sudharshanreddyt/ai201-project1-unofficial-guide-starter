"""
scraper.py
----------
Handles fetching and cleaning of web pages for the GWU unofficial guide.

  fetch_and_save_all(urls)   -- download every URL, save raw + cleaned .txt
  fetch_raw(url)             -- fetch one URL, return raw text
  clean(url, raw)            -- clean one raw text, return cleaned text

For Reddit URLs, old.reddit.com is scraped with requests + BeautifulSoup.
If REDDIT_CLIENT_ID / REDDIT_CLIENT_SECRET are set in .env (via config.py),
the official PRAW OAuth API is used instead for better comment depth.

Output directories (configured in config.py):
  documents/raw/      -- one .txt per URL, saved before any cleaning
  documents/cleaned/  -- one .txt per URL, cleaned and ready for RAG
"""

import re
import time
import html
import logging
from pathlib import Path
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

import config
from documents.doc_urls import DOC_URLS

# ── logging ───────────────────────────────────────────────────────────────────
log = logging.getLogger(__name__)

# ── paths (from config) ───────────────────────────────────────────────────────
DOCS_DIR  = Path(config.DOCS_PATH)
RAW_DIR   = DOCS_DIR / config.RAW_SUBDIR
CLEAN_DIR = DOCS_DIR / config.CLEANED_SUBDIR

RAW_DIR.mkdir(parents=True, exist_ok=True)
CLEAN_DIR.mkdir(parents=True, exist_ok=True)

# ── Reddit OAuth (optional, from config) ──────────────────────────────────────
USE_PRAW = bool(config.REDDIT_CLIENT_ID and config.REDDIT_CLIENT_SECRET)
_praw_reddit = None   # lazy-initialised


def _get_praw():
    global _praw_reddit
    if _praw_reddit is None:
        import praw  # noqa: PLC0415
        _praw_reddit = praw.Reddit(
            client_id=config.REDDIT_CLIENT_ID,
            client_secret=config.REDDIT_CLIENT_SECRET,
            user_agent=config.REDDIT_USER_AGENT,
        )
    return _praw_reddit


# ── request settings ──────────────────────────────────────────────────────────
HEADERS = {
    "User-Agent": config.REDDIT_USER_AGENT,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}
REQUEST_TIMEOUT = 25   # seconds
DELAY_BETWEEN   = 3    # seconds between requests (be polite)

# ── boilerplate detection ─────────────────────────────────────────────────────
JUNK_TAGS = {
    "script", "style", "noscript", "iframe",
    "svg", "path", "symbol", "use",
    "form", "button", "input", "select", "textarea",
    "figure", "figcaption",
}

BOILERPLATE_RE = re.compile(
    r"(nav(?:bar|igation)?|menu|header|footer|sidebar|breadcrumb|"
    r"cookie|banner|modal|overlay|popup|adverti|advert|ads?[-_]|"
    r"share|social[-_]|comment[-_]count|read[-_]?more|related[-_]|"
    r"recommend|promo|newsletter|subscribe|signup|login|search[-_]bar|"
    r"pagination|site[-_]?info|tag[-_]?cloud|widget|utility[-_]bar|"
    r"promotedlink|promoted-link|side[-_]?bar)",
    re.IGNORECASE,
)

# ── file naming ───────────────────────────────────────────────────────────────

def _filename(url: str) -> str:
    """Return a short, human-readable stem from the last URL path segment."""
    parts = [p for p in urlparse(url).path.strip("/").split("/") if p]
    slug = parts[-1] if parts else urlparse(url).netloc
    return re.sub(r"[^A-Za-z0-9_\-]", "_", slug)


# ── fetchers ──────────────────────────────────────────────────────────────────

def fetch_raw(url: str) -> str:
    """
    Fetch *url* and return raw extracted text.

    Reddit: uses PRAW OAuth if credentials are configured, otherwise
    scrapes old.reddit.com with requests + BeautifulSoup.
    Everything else: generic requests + BeautifulSoup.
    """
    if "reddit.com" in url:
        if USE_PRAW:
            log.info("  Using PRAW OAuth API")
            return _fetch_reddit_praw(url)
        log.info("  Using old.reddit.com HTML scrape")
        return _fetch_reddit_old(url)
    return _fetch_generic_html(url)


def _fetch_reddit_praw(url: str) -> str:
    """Fetch a Reddit thread via the official OAuth API (PRAW)."""
    reddit = _get_praw()
    submission = reddit.submission(url=url)
    submission.comments.replace_more(limit=None)

    parts = [f"[POST TITLE] {submission.title}"]
    if submission.selftext.strip():
        parts.append(f"[POST BODY]\n{submission.selftext.strip()}")

    def _walk(comments):
        for c in comments:
            body = getattr(c, "body", "").strip()
            if body and body not in ("[deleted]", "[removed]"):
                parts.append(body)
            if getattr(c, "replies", []):
                _walk(c.replies)

    _walk(submission.comments.list())
    return "\n\n".join(parts)


def _fetch_reddit_old(url: str) -> str:
    """
    Scrape old.reddit.com with BeautifulSoup.

    Scopes post-body extraction to the post's own div.thing.link so the
    subreddit sidebar is never mistaken for the post selftext.
    """
    old_url = url.replace("www.reddit.com", "old.reddit.com").rstrip("/")

    session = requests.Session()
    session.headers.update(HEADERS)
    resp = session.get(old_url, timeout=REQUEST_TIMEOUT)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    parts: list[str] = []

    # Post title — scope to the post container
    post_thing = soup.select_one("div#siteTable div.thing.link")
    title_tag = (
        post_thing.select_one("a.title") if post_thing
        else soup.select_one("a.title")
    )
    if title_tag:
        parts.append(f"[POST TITLE] {title_tag.get_text(strip=True)}")

    # Post selftext — must be scoped to post_thing to avoid grabbing sidebar
    if post_thing:
        selftext_div = post_thing.select_one("div.usertext-body .md")
    else:
        all_md = soup.select("div.usertext-body .md")
        selftext_div = all_md[1] if len(all_md) > 1 else (all_md[0] if all_md else None)

    if selftext_div:
        selftext = selftext_div.get_text(separator=" ", strip=True)
        if selftext:
            parts.append(f"[POST BODY]\n{selftext}")

    # Comments — plain text only, skip deleted
    for comment_div in soup.select("div.comment"):
        if "deleted" in comment_div.get("class", []):
            continue
        body_div = comment_div.select_one("div.usertext-body .md")
        if not body_div:
            continue
        body = body_div.get_text(separator=" ", strip=True)
        if body and body not in ("[deleted]", "[removed]"):
            parts.append(body)

    return "\n\n".join(parts) if parts else ""


def _fetch_generic_html(url: str) -> str:
    """Fetch any non-Reddit page; return raw visible text via BS4."""
    resp = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    return soup.get_text(separator="\n")


# ── cleaners ──────────────────────────────────────────────────────────────────

def _is_boilerplate(tag) -> bool:
    for attr in ("class", "id", "role", "aria-label"):
        values = tag.get(attr, [])
        if isinstance(values, str):
            values = [values]
        for v in values:
            if BOILERPLATE_RE.search(v):
                return True
    return False


def clean(url: str, raw: str) -> str:
    """Clean *raw* text extracted from *url*. Returns cleaned string."""
    if "reddit.com" in url:
        return _clean_reddit(raw)
    return _clean_generic_html(url)


def _clean_reddit(raw: str) -> str:
    """Light clean: decode entities, strip residual HTML, normalise whitespace."""
    text = html.unescape(raw)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return "\n".join(line.rstrip() for line in text.splitlines()).strip()


def _clean_generic_html(url: str) -> str:
    """Full structural clean for non-Reddit pages (re-fetches the page)."""
    resp = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
    soup = BeautifulSoup(resp.text, "html.parser")

    for tag in soup.find_all(JUNK_TAGS):
        tag.decompose()
    for tag in soup.find_all(True):
        try:
            if _is_boilerplate(tag):
                tag.decompose()
        except Exception:
            pass

    text = html.unescape(soup.get_text(separator="\n"))
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return "\n".join(line.strip() for line in text.splitlines() if line.strip()).strip()


# ── main pipeline ─────────────────────────────────────────────────────────────

def fetch_and_save_all(urls: list[str] = DOC_URLS) -> None:
    """
    Fetch every URL, save raw text, clean it, save cleaned text.
    Runs with a polite delay between requests.
    """
    if USE_PRAW:
        log.info("Reddit OAuth credentials found — using PRAW.")
    else:
        log.info("No Reddit credentials — using old.reddit.com HTML scraping.")

    total = len(urls)
    success = 0
    used_names: dict[str, int] = {}

    for idx, url in enumerate(urls, 1):
        base = _filename(url)
        count = used_names.get(base, 0) + 1
        used_names[base] = count
        fname = base if count == 1 else f"{base}_{count}"

        raw_path   = RAW_DIR   / f"{fname}.txt"
        clean_path = CLEAN_DIR / f"{fname}.txt"

        log.info("[%d/%d] Fetching  %s", idx, total, url)

        try:
            raw_text = fetch_raw(url)
        except Exception as exc:
            log.error("  FAILED to fetch %s — %s", url, exc)
            if idx < total:
                time.sleep(DELAY_BETWEEN)
            continue

        if not raw_text.strip():
            log.warning("  Empty response for %s — skipping", url)
            if idx < total:
                time.sleep(DELAY_BETWEEN)
            continue

        raw_path.write_text(f"SOURCE_URL: {url}\n\n{raw_text}", encoding="utf-8")
        log.info("  raw   → %s  (%d chars)", raw_path.name, len(raw_text))

        try:
            cleaned_text = clean(url, raw_text)
        except Exception as exc:
            log.error("  FAILED to clean %s — %s", url, exc)
            if idx < total:
                time.sleep(DELAY_BETWEEN)
            continue

        clean_path.write_text(f"SOURCE_URL: {url}\n\n{cleaned_text}", encoding="utf-8")
        log.info("  clean → %s  (%d chars)", clean_path.name, len(cleaned_text))

        success += 1
        if idx < total:
            time.sleep(DELAY_BETWEEN)

    log.info("Done. %d/%d URLs successfully ingested.", success, total)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s  %(levelname)-8s  %(message)s",
        datefmt="%H:%M:%S",
    )
    fetch_and_save_all()
