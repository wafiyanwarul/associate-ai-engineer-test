# Learning RAG Demo - Refactored

A clean, maintainable implementation of a RAG (Retrieval-Augmented Generation) service demonstrating object-oriented design principles and production-ready architecture patterns.

## 🏗️ Architecture Overview

This project implements a layered architecture with clear separation of concerns:
```
┌─────────────────────────────────────────┐
│           API Layer (api/)              │
│  - FastAPI endpoints                    │
│  - Pydantic request/response models     │
│  - HTTP concerns only                   │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│        Workflow Layer (workflows/)      │
│  - RAG orchestration using LangGraph    │
│  - State management                     │
│  - Coordinates services                 │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│        Services Layer (services/)       │
│  - EmbeddingService: text → vectors     │
│  - DocumentStore: Qdrant + fallback     │
│  - Business logic encapsulation         │
└─────────────────────────────────────────┘
```

## 📁 Project Structure
```
.
├── api/
│   ├── __init__.py          # API package exports
│   ├── models.py            # Pydantic schemas
│   └── routes.py            # Endpoint handlers
├── services/
│   ├── __init__.py          # Services package exports
│   ├── embedding_service.py # Embedding logic
│   └── document_store.py    # Storage logic (Qdrant + fallback)
├── workflows/
│   ├── __init__.py          # Workflows package exports
│   └── rag_workflow.py      # LangGraph orchestration
├── config.py                # Centralized configuration
├── main.py                  # Application entry point
├── .env.example             # Environment variables template
├── .gitignore              # Git ignore rules
├── notes.md                # Refactoring design decisions
└── README.md               # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- (Optional) Qdrant instance running locally

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/wafiyanwarul/associate-ai-engineer-test.git
cd associate-ai-engineer-test
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install fastapi uvicorn pydantic qdrant-client langgraph
```

4. **Configure environment (optional)**
```bash
cp .env.example .env
# Edit .env if needed (defaults work fine for local development)
```

5. **Run the application**
```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`

## 📡 API Endpoints

### 1. Add Document
**POST** `/add`

Add a document to the knowledge base.
```bash
curl -X POST http://127.0.0.1:8000/add \
  -H "Content-Type: application/json" \
  -d '{"text":"LangGraph is awesome for workflows"}'
```

**Response:**
```json
{
  "id": 0,
  "status": "added"
}
```

### 2. Ask Question
**POST** `/ask`

Query the RAG system.
```bash
curl -X POST http://127.0.0.1:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"what is langgraph?"}'
```

**Response:**
```json
{
  "question": "what is langgraph?",
  "answer": "I found this: 'LangGraph is awesome for workflows'",
  "context_used": [
    "LangGraph is awesome for workflows"
  ],
  "latency_sec": 0.023
}
```

### 3. System Status
**GET** `/status`

Check system health and configuration.
```bash
curl http://127.0.0.1:8000/status
```

**Response:**
```json
{
  "qdrant_ready": false,
  "storage_type": "in-memory",
  "document_count": 1,
  "graph_ready": true
}
```

### 4. API Documentation
**GET** `/docs`

Interactive API documentation (Swagger UI) available at `http://127.0.0.1:8000/docs`

## 🔧 Configuration

Configuration is managed through `config.py` and can be customized via environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `QDRANT_URL` | `http://localhost:6333` | Qdrant server URL |
| `QDRANT_COLLECTION` | `demo_collection` | Collection name in Qdrant |
| `EMBEDDING_DIMENSION` | `128` | Vector embedding dimension |
| `SEARCH_LIMIT` | `2` | Max documents returned per search |

## 🏛️ Design Principles

### 1. **Separation of Concerns**
Each layer has a single, well-defined responsibility:
- API layer handles HTTP
- Workflow layer orchestrates operations
- Services layer implements business logic

### 2. **Dependency Injection**
Dependencies are explicitly passed through constructors, making the code testable and the dependency graph clear.

### 3. **Graceful Degradation**
If Qdrant is unavailable, the system automatically falls back to in-memory storage without crashing.

### 4. **Configuration Over Hardcoding**
All environment-specific values are centralized and can be changed without modifying code.

## 🧪 Testing

The architecture supports easy unit testing:
```python
# Example: Testing EmbeddingService independently
from services import EmbeddingService

def test_embedding_dimension():
    service = EmbeddingService(dimension=64)
    result = service.embed("test")
    assert len(result) == 64

# Example: Testing DocumentStore with mock Qdrant
from services import DocumentStore

def test_document_store_fallback():
    # Force fallback by using invalid URL
    store = DocumentStore(qdrant_url="http://invalid:9999")
    assert not store.using_qdrant
    
    # Should still work with in-memory storage
    success = store.add_document(0, "test", [0.1] * 128)
    assert success
```

## 🎯 Key Improvements Over Original

| Aspect | Before | After |
|--------|--------|-------|
| **Structure** | Single 100-line file | Modular 4-layer architecture |
| **Configuration** | Hardcoded values | Centralized config with env support |
| **Dependencies** | Global state | Explicit dependency injection |
| **Testability** | Difficult (global state) | Easy (isolated components) |
| **Maintainability** | Mixed concerns | Clear separation of concerns |
| **Error Handling** | Basic try-catch | Graceful degradation + clear error messages |
| **Documentation** | Minimal | Comprehensive (docstrings + README) |

## 🚦 Production Readiness

While this remains a demo with fake embeddings, the architecture is production-ready:

- ✅ **Scalable**: Each layer can be scaled independently
- ✅ **Maintainable**: Clear structure for team development
- ✅ **Testable**: Components can be unit tested in isolation
- ✅ **Flexible**: Easy to swap implementations (e.g., real embedding models)
- ✅ **Observable**: Structured logging and error handling
- ✅ **Configurable**: Environment-based configuration

## 📚 Next Steps for Production

To deploy this to production with real AI capabilities:

1. **Replace fake embeddings**: Swap `EmbeddingService` with real model (e.g., `sentence-transformers`)
2. **Add authentication**: Implement API key or OAuth
3. **Add persistence**: Configure Qdrant with persistent storage
4. **Add monitoring**: Integrate Prometheus/Grafana
5. **Add rate limiting**: Prevent abuse
6. **Add caching**: Cache frequent queries
7. **Add comprehensive tests**: Unit, integration, and E2E tests

## 📖 Additional Documentation

- **Design decisions**: See `notes.md` for detailed explanation of architectural choices
- **API documentation**: Visit `/docs` endpoint for interactive API explorer

## 🤝 Contributing

This is a technical assessment project. For production use, consider:
- Adding proper error handling for edge cases
- Implementing comprehensive test coverage
- Adding monitoring and observability
- Using production-grade embedding models

## 📄 License

This is a demo project for educational purposes.