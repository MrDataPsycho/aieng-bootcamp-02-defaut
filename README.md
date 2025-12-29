# AI Engineering Bootcamp - Default Track

A comprehensive exploration of building agentic systems with LangGraph, vector search, and LangSmith observability.

## Sprint 3: Pattern for Building Agentic Systems & Single-Turn Agent

**Version:** v3.0.0

### Overview

Sprint 3 focuses on implementing architectural patterns for building production-ready agentic systems. We demonstrate a single-turn agent that can:

- Route incoming questions based on relevance (Intent Router)
- Execute multi-step reasoning with tool orchestration
- Leverage hybrid search (semantic + BM25) for retrieval
- Trace execution with LangSmith for monitoring and debugging
- Provide structured, markdown-formatted responses

### Key Components

#### 1. Multi-Node Agent Architecture
- **Intent Router Node**: Determines question relevance before processing
- **Agent Node**: Orchestrates reasoning and tool execution using GPT models
- **Tool Node**: Executes retrieval and processing tasks
- **Conditional Routing**: Smart flow control based on agent decisions

#### 2. Interactive CLI
```bash
# Single query mode
uv run python src/cli.py --query "best gaming laptops"

# Interactive conversation mode
uv run python src/cli.py
```

#### 3. Environment Configuration
- **Local Development**: Connects to `http://localhost:6333`
- **Docker**: Uses service discovery with `http://qdrant:6333`
- **Automatic**: Environment variables loaded via `load_dotenv()`

#### 4. LangSmith Integration
- Automatic tracing of all `@traceable` decorated functions
- Monitor embeddings, retrieval, and LLM calls
- Track tool execution and reasoning chains

### Technology Stack

- **LangGraph**: Multi-agent workflow orchestration
- **LangSmith**: Observability and trace monitoring
- **Qdrant**: Vector database with hybrid search
- **FastAPI**: Production server
- **Streamlit**: Web UI
- **Docker Compose**: Deployment orchestration

### Running the Application

#### Docker Deployment
```bash
docker-compose up
```

Services:
- FastAPI API: `http://localhost:8000`
- Streamlit UI: `http://localhost:8501`
- Qdrant: `http://localhost:6333`

#### Local Development
```bash
# Install dependencies
uv sync

# Run CLI
uv run python src/cli.py --query "your question here"

# Run interactive mode
uv run python src/cli.py
```

### Project Structure

```
src/
├── cli.py                          # Interactive CLI with typer
├── api/
│   ├── agent/
│   │   ├── __init__.py            # Environment loading
│   │   ├── graph.py               # LangGraph workflow
│   │   ├── agents.py              # Agent and router nodes
│   │   ├── tools.py               # Retrieval tools
│   │   └── utils/
│   ├── core/
│   │   └── config.py              # Configuration management
│   └── app.py                      # FastAPI server
└── chatbot_ui/
    └── app.py                      # Streamlit UI
```

### Agent Flow

```
User Query
    ↓
Intent Router
    ├→ Not Relevant → Return Answer & Exit
    └→ Relevant → Agent Node
        ↓
    Agent Reasoning
        ├→ Final Answer → Exit
        └→ Tool Call → Tool Node
            ↓
        Retrieve Context (Hybrid Search)
            ↓
        Back to Agent Node (Iterate)
```

### Example Usage

```python
from api.agent.graph import run_agent_wrapper

result = run_agent_wrapper("Can I get earphones for myself and a laptop bag?")
print(result["answer"])
print(result["used_context"])
```

### Environment Variables

```env
OPENAI_API_KEY=your-key
GROQ_API_KEY=your-key
GOOGLE_API_KEY=your-key
LANGSMITH_API_KEY=your-key
LANGSMITH_PROJECT=your-project
LANGCHAIN_TRACING_V2=true
QDRANT_URL=http://localhost:6333  # Optional, defaults to localhost
```

### Development Notes

- All environment variables are loaded automatically from `.env` via `api.agent.__init__`
- Qdrant uses hybrid search combining semantic embeddings and BM25
- LangSmith traces capture all decorated function calls for debugging
- The agent supports up to 3 iterations before exiting to prevent infinite loops

### Next Steps

- Multi-turn conversations (memory management)
- Tool expansion and custom tool integration
- Advanced routing strategies
- Performance optimization and caching

---

**Last Updated**: December 29, 2025
**Status**: Sprint 3 Complete ✅
