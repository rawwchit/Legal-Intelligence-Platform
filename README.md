# Legal Intelligence Platform

A backend service for ingesting Indian legal material, converting it into structured legal chunks, indexing those chunks in Qdrant, and retrieving relevant passages through an API.

## Run locally

1. Start Qdrant: `docker run -p 6333:6333 qdrant/qdrant`
2. From `backend`, install dependencies with `uv sync --group dev`.
3. Copy or configure `backend/.env`, then ingest the corpus with `uv run python scripts/ingest_corpus.py`.
4. Start the API with `uv run uvicorn app.main:app --reload`.

Search indexed material at `GET /api/v1/search?query=Article%2021`.

Every push and pull request affecting the backend runs linting and tests in GitHub Actions.
