from app.tools.sql_tool import SQLTool


def test_employee_count():
    sql_tool = SQLTool()

    result = sql_tool.run(
        "SELECT COUNT(*) AS employee_count FROM employees"
    )

    assert "error" not in result
    assert result["row_count"] == 1
    assert result["results"][0]["employee_count"] == 8


def test_engineering_employee_count():
    sql_tool = SQLTool()

    result = sql_tool.run(
        "SELECT COUNT(*) AS employee_count "
        "FROM employees "
        "WHERE department = 'Engineering'"
    )

    assert "error" not in result
    assert result["results"][0]["employee_count"] == 4


def test_finance_employees():
    sql_tool = SQLTool()

    result = sql_tool.run(
        "SELECT name, role "
        "FROM employees "
        "WHERE department = 'Finance'"
    )

    assert "error" not in result
    assert result["row_count"] == 2


def test_employee_records():
    sql_tool = SQLTool()

    result = sql_tool.run(
        "SELECT name, department, role FROM employees"
    )

    assert "error" not in result
    assert result["row_count"] == 8