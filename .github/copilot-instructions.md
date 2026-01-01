## Quick orientation for AI coding agents

This file captures essential, discoverable patterns for productive work in this repository.

- **Big picture**: This repo implements agentic systems (LangGraph workflows + tools) with a FastAPI backend, a Streamlit UI, and Qdrant vector storage and Postgres as persistance memory store for Agent (will be added soon). See [README.md](README.md) for the architecture overview and agent flow.

- **Primary entry points**:
  - API server: [src/api/app.py](src/api/app.py)
  - CLI: [src/cli.py](src/cli.py)
  - Streamlit UI: [src/chatbot_ui/app.py](src/chatbot_ui/app.py)

- **Package & run conventions**:
  - Uses `uv` as the project toolchain. Typical commands:
    - `uv sync` — install dependencies
    - `uv sync --group dev` — install dev deps (notebooks, linters)
    - `uv run python src/cli.py --query "..."` — run the CLI
  - Docker: use `docker-compose up` (see `docker-compose.yaml`). FastAPI runs at `http://localhost:8000`, Streamlit at `http://localhost:8501`, Qdrant at `http://localhost:6333` when using the compose stack.

- **Config & environment**:
  - Environment variables are loaded via `load_dotenv()` from the agent package. Key vars:
    - `OPENAI_API_KEY`, `LANGSMITH_API_KEY`, `LANGSMITH_PROJECT`, `QDRANT_URL`.
  - Service discovery: local dev expects Qdrant at `http://localhost:6333`; Docker uses `http://qdrant:6333`.

- **Agent & tool patterns to follow**:
  - LangGraph workflows live under [src/api/agent/graph.py](src/api/agent/graph.py) and orchestrate nodes defined in [src/api/agent/agents.py](src/api/agent/agents.py).
  - Tool implementations (retrieval, hybrid search) are in [src/api/agent/tools.py](src/api/agent/tools.py). When adding a tool, follow the existing function signatures and ensure LangSmith tracing if external calls are involved.
  - Decorated tracing: functions instrumented for observability use a `@traceable` pattern (LangSmith). Preserve tracing decorators when refactoring to keep observability intact.

- **Search & retrieval specifics**:
  - Vector + BM25 hybrid search is implemented against Qdrant; collections are in `qdrant_storage/collections/`. Use existing config JSON as reference when adding collections.
  - Sample datasets are in `data/` (JSONL files). Use these for local indexing and tests.

- **Code style & pre-commit workflow**:
  - The repo enforces formatting/linting using `ruff`. CLAUDE.md emphasizes running:
    - `uv run ruff format` before commit
    - `uv run ruff` before commit

- **Testing & notebooks**:
  - There are no unit tests in the repo root; exploratory and reproducible examples live in `notebooks/` (see `notebooks/week_5/` for agent demos).
  - For validating changes quickly, prefer reproducing examples from the notebooks or spinning the `docker-compose` stack to exercise end-to-end behavior.

- **Where to add features**:
  - New API routes: use `src/api/api/endpoints.py` and follow the router pattern used by `app.include_router(api_router)` in [src/api/app.py](src/api/app.py).
  - New LangGraph nodes or tools: place code under [src/api/agent/](src/api/agent/) and export small, testable functions that accept and return serializable dicts.

- **Integration touchpoints**:
  - LangSmith tracing: keep trace metadata intact when changing signatures. Traces are used to debug agent reasoning and LLM calls.
  - Qdrant: local collections can be inspected in `qdrant_storage/`.
  - Dockerfiles: `Dockerfile.fastapi` and `Dockerfile.streamlit` indicate build/runtime specifics—follow them when adjusting prod images.

- **Avoid making assumptions**:
  - Do not assume persistence other than `qdrant_storage/` — ephemeral containers will lose local indexes; prefer using the provided `qdrant_storage/collections/` templates when reproducing state.

- **Examples (common tasks)**:
  - Run full stack locally (build & services):

    ```bash
    docker-compose up --build
    # FastAPI: http://localhost:8000
    # Streamlit: http://localhost:8501
    ```

  - Run a single CLI query locally:

    ```bash
    uv sync
    uv run python src/cli.py --query "best gaming laptops"
    ```

- **When editing code**:
  - Preserve LangGraph node I/O shapes and LangSmith tracing decorators.
  - Update `pyproject.toml` only for dependency additions; prefer `uv sync` to refresh local env.
  - If UI changes, bump the version in [src/chatbot_ui/app.py](src/chatbot_ui/app.py) (project convention noted in docs).
  - **Import hygiene**: Remove all unused imports to keep code clean. Conversely, verify that all used modules/classes are properly imported—check both explicitly used items and those used transitively in type annotations, decorators, or function calls.
  - For notebooks, pay special attention to imports in the first code cell; check for unused imports from `qdrant_client.models`, `langgraph.types`, `typing`, and `langchain_core.messages` which often get imported but not used.
  - in the notebook always do `from dotenv import load_dotenv, find_dotenv` and then load the .env file with `load_dotenv(find_dotenv(), override=True)` to ensure environment variables are correctly loaded.

