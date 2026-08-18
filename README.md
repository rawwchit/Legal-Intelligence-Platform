# Legal Intelligence Platform

A backend service for ingesting Indian legal material, converting it into structured legal chunks, indexing those chunks in Qdrant, and retrieving relevant passages through an API.

## Run locally

1. From `backend`, copy `.env.example` to `.env`, then install dependencies with `uv sync --group dev`.
2. The default `QDRANT_PATH="storage/qdrant"` uses local persistent Qdrant storage; Docker is not required.
3. Ingest the corpus with `uv run python -m scripts.ingest_corpus`.
4. Start the API with `uv run uvicorn app.main:app --reload`.

Open `http://127.0.0.1:8000` to use the search interface. Search indexed material programmatically at `GET /api/v1/search?query=Article%2021`.

Every push and pull request affecting the backend runs linting and tests in GitHub Actions.
