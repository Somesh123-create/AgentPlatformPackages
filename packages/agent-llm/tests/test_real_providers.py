import os

import pytest

from agent_llm import Message
from agent_llm.providers.groq import GroqProvider
from agent_llm.providers.nvidia import NVIDIAProvider


@pytest.mark.asyncio
async def test_groq_real_call():

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        pytest.skip("GROQ_API_KEY is not set")

    provider = GroqProvider(
        api_key=api_key
    )

    response = await provider.generate(
        model="groq-gpt-oss-120b",
        messages=[
            Message(
                role="user",
                content="Say hello in one sentence.",
            )
        ],
    )

    print("\n===== GROQ =====")
    print("Provider:", response.provider)
    print("Model:", response.model)
    print("Response:", response.content)
    print("Usage:", response.usage)

    assert response.content


# @pytest.mark.asyncio
# async def test_nvidia_real_call():

    api_key = os.getenv("NVIDIA_API_KEY")

    if not api_key:
        pytest.skip("NVIDIA_API_KEY is not set")

    provider = NVIDIAProvider(
        api_key=api_key
    )

    response = await provider.generate(
        model="YOUR_NVIDIA_MODEL",
        messages=[
            Message(
                role="user",
                content="Say hello in one sentence.",
            )
        ],
    )

    print("\n===== NVIDIA =====")
    print("Provider:", response.provider)
    print("Model:", response.model)
    print("Response:", response.content)
    print("Usage:", response.usage)

    assert response.content