import os
from dotenv import load_dotenv

load_dotenv()

# --- LLM ---
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
LLM_MODEL = "llama-3.3-70b-versatile"

# --- Embeddings ---
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# --- Vector store ---
CHROMA_COLLECTION = "unofficial_guide_bot"
CHROMA_PATH = "./chroma_db"

# --- Retrieval ---
N_RESULTS = 4

# --- Documents ---
DOCS_PATH = "./documents"
RAW_SUBDIR = "raw"
CLEANED_SUBDIR = "cleaned"

# --- Reddit scraper ---
REDDIT_CLIENT_ID     = os.getenv("REDDIT_CLIENT_ID", "")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET", "")
REDDIT_USER_AGENT    = os.getenv("REDDIT_USER_AGENT", "gwu_guide_ingest/1.0 by /u/yourreddituser")

# --- Chunking ---
CHUNK_SIZE    = 500   # target characters per chunk
CHUNK_OVERLAP = 100   # overlap between consecutive chunks
