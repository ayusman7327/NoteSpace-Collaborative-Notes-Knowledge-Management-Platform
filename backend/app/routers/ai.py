from fastapi import APIRouter
from pydantic import BaseModel

from app.services.ai_service import (
    explain_content,
    fix_grammar,
    improve_writing,
    rewrite_content,
    summarize_content,
)


router = APIRouter(
    prefix="/ai",
    tags=["AI"],
)


class AIRequest(BaseModel):
    content: str


class AIResponse(BaseModel):
    result: str


@router.post(
    "/summarize",
    response_model=AIResponse,
)
def summarize(data: AIRequest):
    result = summarize_content(data.content)

    return {
        "result": result,
    }


@router.post(
    "/rewrite",
    response_model=AIResponse,
)
def rewrite(data: AIRequest):
    result = rewrite_content(data.content)

    return {
        "result": result,
    }


@router.post(
    "/improve",
    response_model=AIResponse,
)
def improve(data: AIRequest):
    result = improve_writing(data.content)

    return {
        "result": result,
    }


@router.post(
    "/grammar",
    response_model=AIResponse,
)
def grammar(data: AIRequest):
    result = fix_grammar(data.content)

    return {
        "result": result,
    }


@router.post(
    "/explain",
    response_model=AIResponse,
)
def explain(data: AIRequest):
    result = explain_content(data.content)

    return {
        "result": result,
    }