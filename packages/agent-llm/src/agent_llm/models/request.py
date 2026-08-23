from pydantic import BaseModel, Field
from agent_llm.models.message import Message


class GenerateRequest(BaseModel):
    model: str
    messages: list[Message]
    temperature: float = Field(
        default=0.7,
        ge=0.0,
        le=2.0,
    )
    max_tokens: int | None = None
