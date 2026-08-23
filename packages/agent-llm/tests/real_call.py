import asyncio
import os

from agent_llm import Message
from agent_llm.providers.groq import GroqProvider
from agent_llm.providers.nvidia import NVIDIAProvider


async def test_groq():

    print("\n========== GROQ ==========")

    provider = GroqProvider(
        api_key=os.environ["GROQ_API_KEY"]
    )

    response = await provider.generate(
        model="openai/gpt-oss-20b",
        messages=[
            Message(
                role="user",
                content="Explain Redis in one sentence.",
            )
        ],
    )

    print("Provider:", response.provider)
    print("Model:", response.model)
    print("Answer:", response.content)
    print("Tokens:", response.usage.total_tokens)


async def test_nvidia():

    print("\n========== NVIDIA ==========")

    provider = NVIDIAProvider(
        api_key=os.environ["NVIDIA_API_KEY"]
    )

    response = await provider.generate(
        model="openai/gpt-oss-20b",
        messages=[
            Message(
                role="user",
                content="Explain PostgreSQL in one sentence.",
            )
        ],
    )

    print("Provider:", response.provider)
    print("Model:", response.model)
    print("Answer:", response.content)
    print("Tokens:", response.usage.total_tokens)


async def main():

    # await test_groq()
    await test_nvidia()


if __name__ == "__main__":
    asyncio.run(main())