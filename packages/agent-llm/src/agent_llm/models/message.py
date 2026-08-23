from typing import Literal

from pydantic import BaseModel


MessageRole = Literal[
    "system",
    "user",
    "assistant",
    "tool",
]


class Message(BaseModel):

    role: MessageRole

    content: str