from pydantic import BaseModel, Field


class AIRequest(BaseModel):
    prompt: str = Field(
        min_length=1,
        max_length=10000,
    )


class AIResponse(BaseModel):
    response: str


class WorkspaceAIRequest(BaseModel):
    question: str = Field(
        min_length=1,
        max_length=2000,
    )