from app.agent.llm_router import LLMRouter


def test_routes_calculation():
    router = LLMRouter()

    result = router.route("What is 18 * 12?")

    assert result == "calculator"


def test_routes_sql_employee_count():
    router = LLMRouter()

    result = router.route(
        "How many employees are in Engineering?"
    )

    assert result == "sql"


def test_routes_sql_employee_list():
    router = LLMRouter()

    result = router.route(
        "Who works in Finance?"
    )

    assert result == "sql"


def test_routes_rag_leave_policy():
    router = LLMRouter()

    result = router.route(
        "How many days of annual leave do employees receive?"
    )

    assert result == "rag"


def test_routes_rag_security_policy():
    router = LLMRouter()

    result = router.route(
        "What should employees do if they suspect a security incident?"
    )

    assert result == "rag"


def test_routes_rag_remote_work_policy():
    router = LLMRouter()

    result = router.route(
        "How many days per week can employees work remotely?"
    )

    assert result == "rag"