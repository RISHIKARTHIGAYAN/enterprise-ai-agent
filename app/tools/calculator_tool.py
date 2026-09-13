import ast
import operator


class CalculatorTool:

    OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.Mod: operator.mod,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    def run(self, expression: str):

        try:

            tree = ast.parse(
                expression,
                mode="eval",
            )

            result = self._evaluate(
                tree.body
            )

            return {
                "tool": "calculator",
                "expression": expression,
                "result": result,
            }

        except Exception as error:

            return {
                "tool": "calculator",
                "expression": expression,
                "error": str(error),
            }

    def _evaluate(self, node):

        if isinstance(node, ast.Constant):

            if isinstance(
                node.value,
                (int, float),
            ):
                return node.value

            raise ValueError(
                "Only numeric values are allowed."
            )

        if isinstance(node, ast.UnaryOp):

            operator_function = self.OPERATORS.get(
                type(node.op)
            )

            if operator_function is None:
                raise ValueError(
                    "Unsupported operator."
                )

            return operator_function(
                self._evaluate(node.operand)
            )

        if isinstance(node, ast.BinOp):

            operator_function = self.OPERATORS.get(
                type(node.op)
            )

            if operator_function is None:
                raise ValueError(
                    "Unsupported operator."
                )

            left = self._evaluate(
                node.left
            )

            right = self._evaluate(
                node.right
            )

            return operator_function(
                left,
                right,
            )

        raise ValueError(
            "Invalid mathematical expression."
        )