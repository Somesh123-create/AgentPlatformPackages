# agent-llm Package

A reusable LLM abstraction for AgentPlatform providing unified access to multiple LLM providers.

## Quick Reference

### Key Imports

```python
from agent_llm import Message
from agent_llm.models.response import LLMResponse, Usage
from agent_llm.providers.base import LLMProvider
from agent_llm.routing.router import ProviderRouter
from agent_llm.providers.openai import OpenAIProvider
from agent_llm.providers.groq import GroqProvider
```

### Core Models

- `Message(role, content)` - Pydantic BaseModel with role: "system"|"user"|"assistant"|"tool"
- `LLMResponse(id, provider, model, content, usage, finish_reason)` - Response model
- `Usage(input_tokens, output_tokens, total_tokens)` - Token usage model

### Key Classes

- `LLMClient(provider, model, router)` - Main client with `generate()` and `stream()` methods
- `ProviderRouter(providers)` - Routes requests to registered providers
- `LLMProvider` (ABC) - Abstract base with `generate()` and `stream()` methods

### Provider Implementations

| Provider | Module | Key Setup |
|----------|--------|-----------|
| OpenAI | `providers/openai.py` | `AsyncOpenAI(api_key)` |
| Groq | `providers/groq.py` | `AsyncGroq(api_key)` |
| NVIDIA | `providers/nvidia.py` | Not yet implemented |
| Anthropic | optional dep | `google-genai` or `anthropic` |

### Conventions

- All providers inherit from `LLMProvider` ABC
- Use `Message` model for all message passing
- Token usage tracked via `Usage` model
- Error handling: providers raise on API failures
- Streaming yields `str` chunks asynchronously

### Testing

- Tests in `tests/` directory
- Use `pytest` with `pytest-asyncio`
- Key test files: `test_client.py`, `real_call.py`
- Tests verify Message/LLMResponse construction and provider integration

### Common Pitfalls

- Provider names must match registered names in `ProviderRouter`
- `max_tokens` must be `int | None`, not just `int`
- API keys must be provided at provider instantiation
- Streaming requires async iteration

### Build & Test Commands

```bash
# From project root
cd packages/agent-llm
pip install -e .
pytest  # run all tests
```

### Versioning

The project uses Git tags for version tracking. Current version information:

- **v0.1.0** - Initial release tag (`d470d1408c39d2452aeb768e37969de0a835e322`)
- **HEAD** - Points to latest commit on current branch
- **dev** - Development branch
- **main** - Main production branch

### How to Create a Version Tag

To create a new version tag, follow these steps:

```bash
# From project root
cd packages/agent-llm

# Create an annotated tag
git tag -a v0.2.0 -m "Version 0.2.0 - <description of changes>"

# Push the tag to remote
git push origin v0.2.0
```

### Directory Structure

```
packages/agent-llm/
├── pyproject.toml
├── README.md
├── src/agent_llm/
│   ├── __init__.py
│   ├── client.py
│   ├── exceptions.py
│   ├── models/
│   │   ├── message.py
│   │   └── response.py
│   ├── providers/
│   │   ├── base.py
│   │   ├── openai.py
│   │   ├── groq.py
│   │   └── nvidia.py
│   ├── routing/
│   │   └── router.py
│   ├── retry/       # (empty, for future use)
│   ├── streaming/   # (empty, for future use)
│   └── tools/       # (empty, for future use)
└── tests/
    ├── test_client.py
    ├── real_call.py
    └── test_real_providers.py
```