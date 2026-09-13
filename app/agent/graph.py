import time
import uuid

from langgraph.graph import StateGraph, START, END

from app.logger import logger
from app.agent.state import AgentState
from app.agent.guardrails import Guardrail
from app.agent.llm_router import LLMRouter
from app.services.response_generator import generate_final_answer
from app.tools.rag_tool import RAGTool
from app.tools.calculator_tool import CalculatorTool
from app.tools.sql_tool import SQLTool


class EnterpriseAgentGraph:

    def __init__(self):

        self.guardrail = Guardrail()
        self.router = LLMRouter()
        self.rag_tool = RAGTool()
        self.calculator_tool = CalculatorTool()
        self.sql_tool = SQLTool()

        self.graph = self._build_graph()

    # =========================================================
    # BUILD LANGGRAPH WORKFLOW
    # =========================================================

    def _build_graph(self):

        workflow = StateGraph(AgentState)

        workflow.add_node(
            "guardrail",
            self.guardrail_node,
        )

        workflow.add_node(
            "route",
            self.route_node,
        )

        workflow.add_node(
            "rag",
            self.rag_node,
        )

        workflow.add_node(
            "calculator",
            self.calculator_node,
        )

        workflow.add_node(
            "sql",
            self.sql_node,
        )

        workflow.add_node(
            "response",
            self.response_node,
        )

        workflow.add_edge(
            START,
            "guardrail",
        )

        workflow.add_conditional_edges(
            "guardrail",
            self.guardrail_decision,
            {
                "allowed": "route",
                "blocked": END,
            },
        )

        workflow.add_conditional_edges(
            "route",
            self.select_tool,
            {
                "rag": "rag",
                "calculator": "calculator",
                "sql": "sql",
            },
        )

        workflow.add_edge(
            "rag",
            "response",
        )

        workflow.add_edge(
            "calculator",
            "response",
        )

        workflow.add_edge(
            "sql",
            "response",
        )

        workflow.add_edge(
            "response",
            END,
        )

        return workflow.compile()

    # =========================================================
    # GUARDRAIL NODE
    # =========================================================

    def guardrail_node(self, state: AgentState):

        request_id = state["request_id"]

        result = self.guardrail.check(
            state["question"]
        )

        if not result["allowed"]:

            logger.warning(
                f"request_id={request_id} | "
                f"event=guardrail_blocked"
            )

            return {
                "error": result["reason"],
                "answer": result["reason"],
            }

        logger.info(
            f"request_id={request_id} | "
            f"event=guardrail_passed"
        )

        return {
            "error": None,
        }

    # =========================================================
    # GUARDRAIL DECISION
    # =========================================================

    def guardrail_decision(self, state: AgentState):

        if state.get("error"):

            return "blocked"

        return "allowed"

    # =========================================================
    # ROUTER NODE
    # =========================================================

    def route_node(self, state: AgentState):

        request_id = state["request_id"]

        route = self.router.route(
            state["question"]
        )

        logger.info(
            f"request_id={request_id} | "
            f"event=route_selected | "
            f"route={route}"
        )

        return {
            "route": route,
        }

    # =========================================================
    # TOOL SELECTION
    # =========================================================

    def select_tool(self, state: AgentState):

        return state["route"]

    # =========================================================
    # RAG NODE
    # =========================================================

    def rag_node(self, state: AgentState):

        request_id = state["request_id"]

        start_time = time.perf_counter()

        result = self.rag_tool.run(
            state["question"]
        )

        duration_ms = (
            time.perf_counter() - start_time
        ) * 1000

        logger.info(
            f"request_id={request_id} | "
            f"event=rag_completed | "
            f"retrieval_count="
            f"{result.get('retrieval_count', 0)} | "
            f"source_count="
            f"{len(result.get('sources', []))} | "
            f"duration_ms={duration_ms:.2f}"
        )

        return {
            "tool_result": result,
            "sources": result["sources"],
        }

    # =========================================================
    # CALCULATOR NODE
    # =========================================================

    def calculator_node(self, state: AgentState):

        request_id = state["request_id"]

        expression = (
            state["question"]
            .replace("calculate", "")
            .replace("Calculate", "")
            .replace("compute", "")
            .replace("Compute", "")
            .replace("what is", "")
            .replace("What is", "")
            .strip()
            .rstrip("?.")
        )

        start_time = time.perf_counter()

        result = self.calculator_tool.run(
            expression
        )

        duration_ms = (
            time.perf_counter() - start_time
        ) * 1000

        logger.info(
            f"request_id={request_id} | "
            f"event=calculator_completed | "
            f"success={'error' not in result} | "
            f"duration_ms={duration_ms:.2f}"
        )

        return {
            "tool_result": result,
            "sources": [],
        }

    # =========================================================
    # SQL NODE
    # =========================================================

    def sql_node(self, state: AgentState):

        request_id = state["request_id"]

        normalized = (
            state["question"]
            .lower()
        )

        if "how many employees" in normalized:

            if "engineering" in normalized:

                query = """
                SELECT COUNT(*) AS employee_count
                FROM employees
                WHERE department = 'Engineering'
                """

            elif "finance" in normalized:

                query = """
                SELECT COUNT(*) AS employee_count
                FROM employees
                WHERE department = 'Finance'
                """

            elif "marketing" in normalized:

                query = """
                SELECT COUNT(*) AS employee_count
                FROM employees
                WHERE department = 'Marketing'
                """

            elif "human resources" in normalized:

                query = """
                SELECT COUNT(*) AS employee_count
                FROM employees
                WHERE department = 'Human Resources'
                """

            else:

                query = """
                SELECT COUNT(*) AS employee_count
                FROM employees
                """

        elif (
            "list employees" in normalized
            or "who works" in normalized
        ):

            if "engineering" in normalized:

                query = """
                SELECT name, role
                FROM employees
                WHERE department = 'Engineering'
                """

            elif "finance" in normalized:

                query = """
                SELECT name, role
                FROM employees
                WHERE department = 'Finance'
                """

            elif "marketing" in normalized:

                query = """
                SELECT name, role
                FROM employees
                WHERE department = 'Marketing'
                """

            else:

                query = """
                SELECT name, department, role
                FROM employees
                """

        else:

            query = """
            SELECT employee_id,
                   name,
                   department,
                   role,
                   location,
                   years_at_company
            FROM employees
            """

        start_time = time.perf_counter()

        result = self.sql_tool.run(
            query
        )

        duration_ms = (
            time.perf_counter() - start_time
        ) * 1000

        logger.info(
            f"request_id={request_id} | "
            f"event=sql_completed | "
            f"row_count={result.get('row_count', 0)} | "
            f"success={'error' not in result} | "
            f"duration_ms={duration_ms:.2f}"
        )

        return {
            "tool_result": result,
            "sources": [],
        }

    # =========================================================
    # RESPONSE NODE
    # =========================================================

    def response_node(self, state: AgentState):

        request_id = state["request_id"]

        start_time = time.perf_counter()

        answer = generate_final_answer(
            state["question"],
            state["tool_result"],
        )

        duration_ms = (
            time.perf_counter() - start_time
        ) * 1000

        logger.info(
            f"request_id={request_id} | "
            f"event=response_generated | "
            f"duration_ms={duration_ms:.2f}"
        )

        return {
            "answer": answer
        }

    # =========================================================
    # RUN AGENT
    # =========================================================

    def run(self, question: str):

        request_id = str(
            uuid.uuid4()
        )[:8]

        start_time = time.perf_counter()

        logger.info(
            f"request_id={request_id} | "
            f"event=request_started"
        )

        try:

            initial_state = {
                "question": question,
                "request_id": request_id,
                "route": None,
                "tool_result": None,
                "answer": None,
                "sources": [],
                "error": None,
            }

            result = self.graph.invoke(
                initial_state
            )

            duration_ms = (
                time.perf_counter()
                - start_time
            ) * 1000

            status = (
                "error"
                if result.get("error")
                else "success"
            )

            logger.info(
                f"request_id={request_id} | "
                f"event=request_completed | "
                f"route={result.get('route')} | "
                f"duration_ms={duration_ms:.2f} | "
                f"status={status}"
            )

            return result

        except Exception:

            duration_ms = (
                time.perf_counter()
                - start_time
            ) * 1000

            logger.exception(
                f"request_id={request_id} | "
                f"event=request_failed | "
                f"duration_ms={duration_ms:.2f}"
            )

            raise

    # =========================================================
    # CLOSE RESOURCES
    # =========================================================

    def close(self):

        self.sql_tool.close()