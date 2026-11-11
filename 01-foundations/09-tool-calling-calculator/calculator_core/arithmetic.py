"""Safe arithmetic evaluation using a deliberately small Python AST allowlist."""

import ast
from decimal import Decimal, DivisionByZero, InvalidOperation, localcontext

MAX_LENGTH, MAX_NODES, MAX_EXPONENT = 256, 40, 8
MAX_RESULT = Decimal("1e100")


class CalculationError(ValueError):
    """The expression is invalid or outside the calculator's supported subset."""


def _evaluate(node: ast.AST) -> Decimal:
    if isinstance(node, ast.Constant):
        if isinstance(node.value, bool) or not isinstance(node.value, (int, float)):
            raise CalculationError("only numeric literals are supported")
        value = Decimal(str(node.value))
        if not value.is_finite() or abs(value) > MAX_RESULT:
            raise CalculationError("numeric literal outside supported range")
        return value

    if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
        value = _evaluate(node.operand)
        return value if isinstance(node.op, ast.UAdd) else -value

    if isinstance(node, ast.BinOp):
        left, right = _evaluate(node.left), _evaluate(node.right)
        if isinstance(node.op, ast.Add):
            return left + right
        if isinstance(node.op, ast.Sub):
            return left - right
        if isinstance(node.op, ast.Mult):
            return left * right
        if isinstance(node.op, ast.Div):
            return left / right
        if isinstance(node.op, ast.FloorDiv):
            return left // right
        if isinstance(node.op, ast.Mod):
            return left % right
        if isinstance(node.op, ast.Pow):
            if right != right.to_integral_value() or abs(right) > MAX_EXPONENT:
                raise CalculationError("exponent must be an integer from -8 to 8")
            return left ** int(right)

    raise CalculationError(f"unsupported expression element: {type(node).__name__}")


def calculate(expression: str) -> str:
    if not isinstance(expression, str) or not expression.strip():
        raise CalculationError("expression must be non-empty")
    if len(expression) > MAX_LENGTH:
        raise CalculationError("expression too long")

    try:
        tree = ast.parse(expression, mode="eval")
    except SyntaxError as exc:
        raise CalculationError("invalid arithmetic expression") from exc

    if sum(1 for _ in ast.walk(tree)) > MAX_NODES:
        raise CalculationError("expression too complex")

    with localcontext() as ctx:
        ctx.prec = 28
        try:
            result = _evaluate(tree.body)
        except (DivisionByZero, InvalidOperation, ZeroDivisionError, OverflowError) as exc:
            raise CalculationError("undefined arithmetic operation") from exc

    if not result.is_finite() or abs(result) > MAX_RESULT:
        raise CalculationError("result outside supported range")
    result = result.normalize()
    return format(result, "f") if result else "0"
