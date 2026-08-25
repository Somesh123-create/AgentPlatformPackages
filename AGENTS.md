# AgentPlatform

A unified platform for LLM-powered applications with authentication and database infrastructure.

## Overview

This workspace contains three core packages that provide a complete foundation for building LLM-powered applications:

- **`agent-llm`** - LLM abstraction layer with provider routing
- **`agent-auth`** - Authentication and JWT management
- **`agent-db`** - Database infrastructure with SQLAlchemy ORM

## Package Structure

```text
packages/
├── agent-auth/       # Authentication & JWT
├── agent-db/         # Database & ORM
└── agent-llm/        # LLM abstraction & provider routing
```

Each package has its own `pyproject.toml`, dependencies, and test suite.

## Build & Test Commands

### From workspace root

```bash
# Install all packages in development mode
cd packages/agent-llm && pip install -e .
cd packages/agent-auth && pip install -e .
cd packages/agent-db && pip install -e .

# Run all tests
cd packages/agent-llm && pytest
cd packages/agent-auth && pytest
cd packages/agent-db && pytest
```

### Individual package tests

- `agent-llm`: Tests LLM client, provider routing, message/response models
- `agent-auth`: Tests JWT manager, authentication flows
- `agent-db`: Tests database operations, ORM models

## Key Conventions

### LLM Provider Pattern (`agent-llm`)

- All providers inherit from `LLMProvider` ABC with `generate()` and `stream()` methods
- Use `ProviderRouter` to route requests to available providers
- `Message` model (pydantic BaseModel) is used for all message passing
- Token usage tracked via `Usage` model with `input_tokens`, `output_tokens`, `total_tokens`
- Provider names must match registered names in `ProviderRouter`
- `max_tokens` must be `int | None`, not just `int`
- API keys are provided at provider instantiation
- Streaming yields `str` chunks asynchronously

### Authentication (`agent-auth`)

- `JWTManager` handles token creation and validation
- `CurrentUser` dataclass (frozen) represents authenticated user with `user_id` and `role`
- Uses `python-jose[cryptography]` for JWT operations
- Tokens expire after configurable duration (default: 30 minutes)

### Database (`agent-db`)

- `Base` class extends `sqlalchemy.orm.DeclarativeBase`
- `Database` class manages async engine and session factory
- Uses `asyncpg` for PostgreSQL async driver
- `session()` generator yields `AsyncSession` objects
- Always call `dispose()` to clean up engine connections

### Cross-Cutting Concerns

- All packages require Python >= 3.12
- Dependencies are declared in each package's `pyproject.toml`
- Tests use `pytest` with `pytest-asyncio` for async packages
- Type hints are used extensively (Literal types, type overloads)

## Common Pitfalls

### LLM Provider

- Provider names must match registered names in `ProviderRouter`
- `max_tokens` must be `int | None`, not just `int`
- API keys must be provided at provider instantiation
- Streaming requires async iteration with `async for`
- Unsupported provider will raise `ValueError`

### Authentication

- Secret key must be kept secure and not hardcoded
- Token expiration should be configured per application needs
- Role-based access control uses `CurrentUser.role` field

### Database

- Engine must be disposed of properly to close connections
- Async session factory should not be created per-request
- Pool pre-ping enabled to detect dropped connections

## Quick Reference: Key Imports

### agent-llm

```python
from agent_llm import Message
from agent_llm.models.response import LLMResponse, Usage
from agent_llm.providers.base import LLMProvider
from agent_llm.routing.router import ProviderRouter
from agent_llm.providers.openai import OpenAIProvider
from agent_llm.providers.groq import GroqProvider
```

### agent-auth

```python
from agent_auth.models import CurrentUser
from agent_auth.jwt import JWTManager
```

### agent-db

```python
from agent_db.base import Base
from agent_db.database import Database
```

## Directory Structure (per package)

```
packages/<package>/
├── pyproject.toml
├── src/<package>/
│   ├── __init__.py
│   ├── client.py (or base.py, models.py, etc.)
│   ├── exceptions.py
│   ├── models/ (if applicable)
│   ├── providers/ (agent-llm only)
│   ├── routing/ (agent-llm only)
│   ├── retry/       # (empty, for future use)
│   ├── streaming/   # (empty, for future use)
│   └── tools/       # (empty, for future use)
└── tests/
```

## Related Documentation

- Each package's `README.md` for detailed setup instructions
- `pyproject.toml` for dependency management
- Individual package docs for API reference