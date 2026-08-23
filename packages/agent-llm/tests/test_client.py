from agent_llm import Message
from agent_llm.models.response import (
    LLMResponse,
    Usage,
)


def test_message():

    message = Message(
        role="user",
        content="Hello",
    )

    assert message.role == "user"
    assert message.content == "Hello"


def test_response():

    response = LLMResponse(
        provider="openai",
        model="test-model",
        content="Hello",
        usage=Usage(
            input_tokens=10,
            output_tokens=5,
            total_tokens=15,
        ),
    )

    assert response.provider == "openai"
    assert response.usage.total_tokens == 15