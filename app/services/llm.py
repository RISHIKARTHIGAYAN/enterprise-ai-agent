import ollama

from app.config import LLM_MODEL


SYSTEM_PROMPT = """
You are an enterprise knowledge assistant.

Answer questions using ONLY the supplied context.

Rules:

1. Do not invent facts.
2. Do not use information outside the supplied context.
3. If the context does not contain enough information,
   clearly say that the information was not found
   in the knowledge base.
4. Give concise and professional answers.
5. Cite the source document using:
   [Source: filename]
"""


def generate_answer(
    question: str,
    context: str,
) -> str:

    prompt = f"""
{SYSTEM_PROMPT}

CONTEXT:
{context}

USER QUESTION:
{question}

ANSWER:
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

    return response["message"]["content"]