import os

from fastapi import HTTPException, status
from google import genai
from sqlalchemy.orm import Session

from app.repositories.page_repository import get_workspace_pages


api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError(
        "GEMINI_API_KEY is not configured"
    )

client = genai.Client(
    api_key=api_key
)


def ask_workspace_ai(
    db: Session,
    workspace_id: int,
    question: str,
) -> str:
    pages = get_workspace_pages(
        db=db,
        workspace_id=workspace_id,
    )

    if not pages:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No pages found in this workspace",
        )

    workspace_context = []

    for page in pages:
        clean_content = (
            page.content
            .replace("<p>", "")
            .replace("</p>", "\n")
            .replace("<br>", "\n")
        )

        workspace_context.append(
            f"""
Page Title: {page.title}

Content:
{clean_content}
"""
        )

    context_text = "\n\n---\n\n".join(
        workspace_context
    )

    prompt = f"""
You are NoteSpace AI.

Answer the user's question using only the workspace notes provided below.

If the answer is not present in the notes, say:
"I couldn't find that information in this workspace."

Workspace Notes:

{context_text}

User Question:
{question}

Give a clear and useful answer.
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        if not response.text:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="AI returned an empty response",
            )

        return response.text

    except HTTPException:
        raise

    except Exception as error:
        print(
            "Workspace AI error:",
            error,
        )

        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Unable to generate workspace AI response",
        )