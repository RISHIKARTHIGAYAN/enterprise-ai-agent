import re

from langchain_ollama import ChatOllama
from app.config import LLM_MODEL


class LLMRouter:
    """
    Hybrid router.

    High-confidence patterns are handled deterministically.
    Ambiguous questions are classified by the local LLM.
    """

    def __init__(self):
        self.llm = ChatOllama(
            model=LLM_MODEL,
            temperature=0,
        )

    def route(self, question: str) -> str:
        normalized = question.lower().strip()

        # -----------------------------------------
        # 1. Calculator — deterministic detection
        # -----------------------------------------
        calculator_patterns = [
            r"\d+\s*[\+\-\*\/\%]\s*\d+",
            r"\d+\s*\*\*\s*\d+",
            r"\bcalculate\b",
            r"\bcompute\b",
        ]

        if any(re.search(pattern, normalized) for pattern in calculator_patterns):
            return "calculator"

        # -----------------------------------------
        # 2. SQL — high-confidence employee queries
        # -----------------------------------------
        sql_patterns = [
            r"\bhow many employees\b",
            r"\bemployee count\b",
            r"\bnumber of employees\b",
            r"\blist employees\b",
            r"\bwho works in\b",
            r"\bwhich employees\b",
            r"\bemployees in\b",
            r"\bemployee records\b",
        ]

        if any(re.search(pattern, normalized) for pattern in sql_patterns):
            return "sql"

        # -----------------------------------------
        # 3. Otherwise ask the local LLM
        # -----------------------------------------
        prompt = f"""
You are an enterprise AI routing classifier.

Choose exactly ONE route:

rag
calculator
sql

ROUTES:

rag:
Company policies, rules, procedures, security,
leave, expenses, travel policies, and document knowledge.

calculator:
Mathematical calculations.

sql:
Employee database information such as employee records,
departments, roles, locations, and employee counts.

Examples:

"What is the annual leave policy?" -> rag
"How many days of annual leave do employees receive?" -> rag
"What should I do about a security incident?" -> rag
"Calculate 18 * 12" -> calculator
"How many employees are in Engineering?" -> sql
"Who works in Finance?" -> sql
"List employees in Bangalore" -> sql

If uncertain, choose rag.

Return ONLY:
rag
calculator
sql

QUESTION:
{question}

ROUTE:
"""

        response = self.llm.invoke(prompt)

        route = response.content.strip().lower()
        route = route.replace("`", "").strip()

        if route not in {"rag", "calculator", "sql"}:
            return "rag"

        return route