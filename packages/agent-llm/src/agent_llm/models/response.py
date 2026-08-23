from pydantic import BaseModel


class Usage(BaseModel):
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0


class LLMResponse(BaseModel):
    id: str | None = None
    provider: str
    model: str
    content: str
    usage: Usage
    finish_reason: str | None = None