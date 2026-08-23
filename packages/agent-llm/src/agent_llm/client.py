from collections.abc import AsyncIterator

from agent_llm.models.message import Message
from agent_llm.models.response import LLMResponse
from agent_llm.routing.router import ProviderRouter


class LLMClient:

    def __init__(
            self,
            provider: str,
            model: str,
            router: ProviderRouter,
        ):
        self.provider = provider
        self.model = model
        self.router = router


    async def generate(
            self,
            messages: list[Message],
            temperature: float = 0.7,
            max_tokens: int | None = None,
        ) -> LLMResponse:

        provider = self.router.get_provider(
            self.provider
        )

        return await provider.generate(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )


    async def stream(
            self,
            messages: list[Message],
            temperature: float = 0.7,
            max_tokens: int | None = None,
        ) -> AsyncIterator[str]:

        provider = self.router.get_provider(
            self.provider
        )

        async for chunk in provider.stream(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        ):
            yield chunk