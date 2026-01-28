# Refactoring Notes

## Design Decisions

The original implementation was functional but contained several anti-patterns common in early-stage prototypes: global state management, tight coupling between components, and mixed concerns within a single file. I restructured the codebase around three core principles:

**1. Separation of Concerns via Layered Architecture**

I implemented a clear three-layer architecture:
- **Services Layer** (`services/`): Handles business logic for embeddings and document storage
- **Workflow Layer** (`workflows/`): Orchestrates services using LangGraph for state management
- **API Layer** (`api/`): Manages HTTP concerns with request/response validation

This separation makes each component independently testable and allows teams to work on different layers without conflicts. For example, the embedding implementation can be swapped from fake to production (e.g., sentence-transformers) by simply replacing `EmbeddingService` without touching API or workflow code.

**2. Dependency Injection Over Global State**

Instead of global variables (`qdrant`, `docs_memory`), dependencies are now explicitly injected through constructors. The `main.py` acts as a composition root, wiring up all dependencies:
```python
embedding_service = EmbeddingService()
document_store = DocumentStore()
workflow = RagWorkflow(embedding_service, document_store)
api = RagAPI(workflow)
```

This makes testing straightforward—mock objects can be injected without modifying production code. It also makes the dependency graph explicit and prevents hidden coupling.

**3. Configuration Management**

All environment-specific settings are centralized in `config.py` with validation. This eliminates magic numbers scattered throughout the code and supports different deployment environments (dev/staging/production) through environment variables.

## Trade-offs Considered

The main trade-off was **simplicity vs. flexibility**. I could have introduced more abstraction layers (e.g., repository pattern for storage, strategy pattern for embeddings), but this would add complexity without clear immediate benefit for a demo application.

I chose pragmatic OOP that balances clean architecture principles with code readability. The current structure is production-ready in the sense that it can scale to real use cases, but it doesn't over-engineer for hypothetical future requirements.

For instance, `DocumentStore` handles both Qdrant and in-memory fallback within a single class. A more enterprise approach might use separate implementations with a shared interface, but for this scale, the current approach provides graceful degradation without unnecessary abstraction overhead.

## Maintainability Improvements

The refactored version improves maintainability in several concrete ways:

1. **Isolated Testing**: Each component can be unit tested independently. You can test `EmbeddingService` without running FastAPI or Qdrant.

2. **Clear Responsibilities**: When a bug occurs, the layered structure immediately narrows down where to look. Storage issues? Check `DocumentStore`. API validation errors? Check `api/models.py`.

3. **Safe Refactoring**: The explicit interfaces between layers act as contracts. You can refactor `DocumentStore`'s internal implementation without worrying about breaking the workflow or API layers, as long as the public methods remain compatible.

4. **Onboarding Speed**: New developers can understand the system by reading just the layer they need to work on, rather than untangling a single monolithic file.

5. **Production Readiness**: The structure supports standard DevOps practices—environment-based configuration, graceful error handling, and clear separation that aligns with microservices patterns if scaling is needed.

The external API behavior remains identical to the original implementation, preserving all existing functionality while providing a foundation for sustainable development.