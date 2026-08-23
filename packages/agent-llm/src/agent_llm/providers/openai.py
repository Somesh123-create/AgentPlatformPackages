from collections.abc import AsyncIterator

from openai import AsyncOpenAI

from agent_llm.models.message import Message
from agent_llm.models.response import (
    LLMResponse,
    Usage,
)
from agent_llm.providers.base import LLMProvider


class OpenAIProvider(LLMProvider):
    def __init__(self, api_key: str):
        self.client = AsyncOpenAI(api_key=api_key)
        
    
    async def generate(
            self,
            model: str,
            messages: list[Message],
            temperature: float = 0.7,
            max_tokens: int | None = None,
        ) -> LLMResponse:
        
        request = {
            "model": model,
            "messages": [message.model_dump() for message in messages],
            "temperature": temperature
        }
        
        if max_tokens is not None:
            request["max_tokens"] = max_tokens
            
        response = await self.client.chat.completions.create(**request)
        
        usage = response.usage
        
        return LLMResponse(
            id=response.id,
            provider="openai",
            model=model,
            content=(
                response.choices[0].message.content
                or ""
            ),
            usage=Usage(
                input_tokens=(
                    usage.prompt_tokens
                    if usage
                    else 0
                ),
                output_tokens=(
                    usage.completion_tokens
                    if usage
                    else 0
                ),
                total_tokens=(
                    usage.total_tokens
                    if usage
                    else 0
                ),
            ),
            finish_reason=(
                response.choices[0].finish_reason
            ),
        )
        
    async def stream(
            self,
            model: str,
            messages: list[Message],
            temperature: float = 0.7,
            max_tokens: int | None = None,
        ) -> AsyncIterator[str]:

        request = {
            "model": model,
            "messages": [
                message.model_dump()
                for message in messages
            ],
            "temperature": temperature,
            "stream": True,
        }

        if max_tokens is not None:
            request["max_tokens"] = max_tokens

        response = await self.client.chat.completions.create(
            **request
        )

        async for chunk in response:

            if not chunk.choices:
                continue

            content = chunk.choices[0].delta.content

            if content:
                yield content