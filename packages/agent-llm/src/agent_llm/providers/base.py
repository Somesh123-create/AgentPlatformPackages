from abc import ABC, abstractmethod
from collections.abc import AsyncIterator

from agent_llm.models.message import Message
from agent_llm.models.response import LLMResponse

class LLMProvider(ABC):

    @abstractmethod
    async def generate(
            self,
            model: str,
            messages: list[Message],
            temperature: float = 0.7,
            max_tokens: int | None = None,
        ) -> LLMResponse:
        ...


    @abstractmethod
    async def stream(
            self,
            model: str,
            messages: list[Message],
            temperature: float = 0.7,
            max_tokens: int | None = None,
        ) -> AsyncIterator[str]:
        ...
