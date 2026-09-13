import re


class Guardrail:
    """
    Lightweight input guardrail for the enterprise agent.

    Blocks obvious prompt-injection and system-information
    extraction attempts before they reach the agent.
    """

    BLOCKED_PATTERNS = [
        r"ignore previous instructions",
        r"ignore all previous instructions",
        r"disregard previous instructions",
        r"disregard all previous instructions",
        r"forget your instructions",
        r"reveal your system prompt",
        r"show me your system prompt",
        r"print your system prompt",
        r"reveal the system message",
        r"show me the system message",
        r"what are your hidden instructions",
        r"reveal hidden instructions",
	r"show me your hidden instructions",
        r"bypass your restrictions",
        r"bypass security",
    ]

    def check(self, question: str):
        if not question or not question.strip():
            return {
                "allowed": False,
                "reason": "The question cannot be empty.",
            }

        normalized = question.lower().strip()

        for pattern in self.BLOCKED_PATTERNS:
            if re.search(pattern, normalized):
                return {
                    "allowed": False,
                    "reason": "The request was blocked by the security guardrail.",
                }

        return {
            "allowed": True,
            "reason": None,
        }