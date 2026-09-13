import ollama

from app.config import LLM_MODEL


SYSTEM_PROMPT = """
You are the final response generator for an enterprise AI assistant.

Your job is to convert the result of an internal tool into a clear,
concise answer for the user.

Rules:

1. Use ONLY the supplied tool result.
2. Never invent information.
3. Do not expose SQL queries, internal implementation details,
   routing logic, or tool names unless explicitly asked.
4. For calculator results, return the numerical answer clearly.
5. For employee database results, summarize the result naturally.
6. For knowledge-base answers, preserve source citations.
7. If the tool reports an error, explain that the request could
   not be completed.
8. Keep the answer professional and concise.
"""


def generate_final_answer(question: str, tool_result: dict) -> str:
    prompt = f"""
{SYSTEM_PROMPT}

USER QUESTION:
{question}

TOOL RESULT:
{tool_result}

FINAL ANSWER:
"""

    response = ollama.chat(
        model=LLM_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    return response["message"]["content"].strip()