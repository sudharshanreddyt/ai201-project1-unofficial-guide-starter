"""
app.py
------
Gradio chat interface for the GW Freshman Guide Bot.

Startup behaviour:
  - Checks if ChromaDB is already populated; if not, runs ingestion.
  - Launches the Gradio UI.

Run with:
    python app.py
"""

import gradio as gr

from ingest import load_documents, chunk_document
from retrieval import embed_and_store, retrieve, get_collection
from generator import generate_response


# ---------------------------------------------------------------------------
# Ingestion — runs once on startup
# ---------------------------------------------------------------------------

def run_ingestion():
    """
    Load GWU Guide documents, chunk them, and store in ChromaDB.

    If the vector store is already populated, ingestion is skipped.
    To re-ingest (e.g. after changing your chunking strategy), delete the
    ./chroma_db folder and restart the app.
    """
    collection = get_collection()

    if collection.count() > 0:
        print(f"Vector store already populated ({collection.count()} chunks). Skipping ingestion.")
        print("To re-ingest, delete the ./chroma_db folder and restart.")
        return

    print("Ingesting GWU Guide documents...")
    documents = load_documents()
    all_chunks = []

    for doc in documents:
        # chunk_document now accepts the full doc dict and carries all
        # metadata (source_url, doc_title, post_body) into every chunk.
        chunks = chunk_document(doc)
        all_chunks.extend(chunks)

    print(f"Total: {len(all_chunks)} chunks from {len(documents)} documents.")

    if all_chunks:
        embed_and_store(all_chunks)
        print(f"Ingestion complete. {len(all_chunks)} chunks stored.")
    else:
        print(
            "\nNo chunks produced. Make sure chunk_document() is implemented in ingest.py.\n"
            "GW Guide Bot will start, but won't be able to answer questions yet.\n"
        )


# ---------------------------------------------------------------------------
# Chat handler
# ---------------------------------------------------------------------------

def chat(message, history):
    """Pass the user's message through the RAG pipeline and return the answer."""
    if not message.strip():
        return ""
    retrieved = retrieve(message)
    return generate_response(message, retrieved)


# ---------------------------------------------------------------------------
# Gradio UI — single gr.Blocks definition
# ---------------------------------------------------------------------------

with gr.Blocks(title="GW Freshman Guide Bot") as demo:

    gr.HTML("""
        <div style="text-align:center; padding:1.25rem 0 0.5rem;">
            <h1 style="font-size:2rem; font-weight:700; color:#312e81; margin:0;">
                GW Freshman Guide Bot
            </h1>
            <p style="color:#6b7280; font-size:1rem; margin:0.4rem 0 0;">
                Ask anything about GWU life from a student's perspective.
            </p>
        </div>
    """)

    with gr.Row():
        with gr.Column(scale=3):
            gr.ChatInterface(
                fn=chat,
                chatbot=gr.Chatbot(
                    height=440,
                    placeholder=(
                        "<div style='text-align:center; color:#9ca3af; margin-top:3rem;'>"
                        "Ask a question about GWU life to get started 🎯"
                        "</div>"
                    ),
                ),
                textbox=gr.Textbox(
                    placeholder='e.g. "What do students say about the D.C. Metro system?"',
                    container=False,
                    scale=7,
                ),
                examples=[
                    "What do students say about the pacing and rigor of early computer science classes at GWU?",
                    "Is the freshman housing lottery actually random, or does the placement matrix favor certain preferences?",
                    "What are the best strategies for navigating the high-stress course registration process at GWU?",
                    "What are the realistic pros and cons of living on the Mount Vernon campus versus Foggy Bottom?",
                    "What do students say about the quality and variety of food at GWU dining halls?"
                ],
                cache_examples=False,
            )

        with gr.Column(scale=1, min_width=180):
            gr.HTML("""
                <div style="background:#f5f3ff; border:1px solid #ddd6fe;
                            border-radius:10px; padding:1rem; margin-top:0.5rem;">
                    <p style="font-size:0.8rem; font-weight:700; color:#4c1d95;
                               margin:0 0 0.5rem; letter-spacing:0.05em;">
                        📚 SOURCES
                    </p>
                    <ul style="font-size:0.85rem; color:#5b21b6; list-style:none;
                                padding:0; margin:0; line-height:1.8;">
                        <li>💻 CS at GWU</li>
                        <li>🏠 Housing &amp; Dorms</li>
                        <li>📝 Course Registration</li>
                        <li>🍽️ Dining</li>
                        <li>📍 Study Spots</li>
                        <li>🎉 Social Scene</li>
                        <li>🚇 Commuting</li>
                        <li>🔒 Campus Safety</li>
                    </ul>
                    <hr style="border:none; border-top:1px solid #ddd6fe; margin:0.75rem 0;">
                    <p style="font-size:0.75rem; color:#7c3aed; margin:0; line-height:1.5;">
                        Answers are grounded in real Reddit posts by GWU students.
                        If information isn't in the sources, the bot will say so.
                    </p>
                </div>
            """)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("  GW Guide Bot — starting up")
    print("=" * 50 + "\n")

    run_ingestion()
    demo.launch(theme=gr.themes.Soft(primary_hue="indigo"))
