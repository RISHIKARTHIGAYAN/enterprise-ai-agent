from app.tools.calculator_tool import CalculatorTool


def test_addition():
    calculator = CalculatorTool()

    result = calculator.run("25 + 17")

    assert result["result"] == 42


def test_multiplication():
    calculator = CalculatorTool()

    result = calculator.run("18 * 12")

    assert result["result"] == 216


def test_division():
    calculator = CalculatorTool()

    result = calculator.run("100 / 4")

    assert result["result"] == 25


def test_power():
    calculator = CalculatorTool()

    result = calculator.run("2 ** 5")

    assert result["result"] == 32


def test_parentheses():
    calculator = CalculatorTool()

    result = calculator.run("(10 + 5) * 3")

    assert result["result"] == 45


def test_invalid_expression():
    calculator = CalculatorTool()

    result = calculator.run("hello")

    assert "error" in result