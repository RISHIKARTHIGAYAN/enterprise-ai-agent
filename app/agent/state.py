from typing import Any, Dict, List, Optional

from typing_extensions import TypedDict


class AgentState(TypedDict):
    question: str
    request_id: str
    route: Optional[str]
    tool_result: Optional[Dict[str, Any]]
    answer: Optional[str]
    sources: List[Dict[str, Any]]
    error: Optional[str]