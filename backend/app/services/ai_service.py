import os

from dotenv import load_dotenv
from google import genai


load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = None

if GEMINI_API_KEY:
    client = genai.Client(api_key=GEMINI_API_KEY)


def generate_ai_response(prompt: str) -> str:
    if not GEMINI_API_KEY or client is None:
        return "Gemini API key is not configured."

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        if response.text:
            return response.text.strip()

        return "No response was generated."

    except Exception as error:
        print("Gemini error:", error)
        return "Unable to generate AI response right now."


def summarize_content(content: str) -> str:
    prompt = f"""
Summarize the following NoteSpace page clearly and concisely.

Content:
{content}
"""

    return generate_ai_response(prompt)


def rewrite_content(content: str) -> str:
    prompt = f"""
Rewrite the following content so that it is clearer,
more professional, and easier to understand.

Keep the original meaning.

Content:
{content}
"""

    return generate_ai_response(prompt)


def improve_writing(content: str) -> str:
    prompt = f"""
Improve the writing quality of the following content.

Make it:
- clear
- professional
- concise
- well structured

Do not change the original meaning.

Content:
{content}
"""

    return generate_ai_response(prompt)


def fix_grammar(content: str) -> str:
    prompt = f"""
Correct the grammar, spelling, punctuation,
and sentence structure of the following content.

Return only the corrected version.

Content:
{content}
"""

    return generate_ai_response(prompt)


def explain_content(content: str) -> str:
    prompt = f"""
Explain the following content in simple and
easy-to-understand language.

Content:
{content}
"""

    return generate_ai_response(prompt)