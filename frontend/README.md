# LexIntel frontend

This interface is served automatically by the local backend API.

1. Configure the local Qdrant path and index the corpus from `backend` with `uv run python -m scripts.ingest_corpus`.
2. Start the API: `uv run uvicorn app.main:app --reload`.
3. Open `http://127.0.0.1:8000`.
