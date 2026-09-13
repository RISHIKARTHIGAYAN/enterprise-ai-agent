from app.agent.graph import EnterpriseAgentGraph


def test_graph_rag_route():
    agent = EnterpriseAgentGraph()

    result = agent.run(
        "How many days of annual leave do employees receive?"
    )

    assert result["route"] == "rag"
    assert result["answer"]
    assert result["error"] is None


def test_graph_calculator_route():
    agent = EnterpriseAgentGraph()

    result = agent.run(
        "What is 18 * 12?"
    )

    assert result["route"] == "calculator"
    assert result["answer"]
    assert result["error"] is None


def test_graph_sql_route():
    agent = EnterpriseAgentGraph()

    result = agent.run(
        "How many employees are in Engineering?"
    )

    assert result["route"] == "sql"
    assert result["answer"]
    assert result["error"] is None