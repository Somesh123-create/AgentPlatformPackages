class AgentLLMError(Exception):
    """Base exception for agent-llm."""


class ProviderNotFoundError(AgentLLMError):
    """Provider is not configured."""


class LLMGenerationError(AgentLLMError):
    """LLM generation failed."""


class LLMTimeoutError(AgentLLMError):
    """LLM request timed out."""


class LLMRateLimitError(AgentLLMError):
    """LLM provider rate limit reached."""