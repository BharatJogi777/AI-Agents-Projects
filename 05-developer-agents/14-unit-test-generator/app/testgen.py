"""Render pytest test templates from explicit function contracts."""
from __future__ import annotations
import keyword
import json
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class TestCase:
    name: str
    category: str
    input_expression: str
    expected_expression: str | None


def generate_cases(function_name: str, examples: list[dict], invalid_inputs: list[str] | None = None) -> list[TestCase]:
    if not isinstance(function_name, str) or not function_name.isidentifier() or keyword.iskeyword(function_name):
        raise ValueError("function_name must be a valid Python identifier")
    if not isinstance(examples, list):
        raise TypeError("examples must be a list")
    cases = []
    for index, item in enumerate(examples):
        if not isinstance(item, dict) or "input" not in item or "expected" not in item:
            raise ValueError("each example requires input and expected expressions")
        if not all(isinstance(item[k], str) and item[k].strip() for k in ("input", "expected")):
            raise ValueError("example expressions must be non-empty strings")
        cases.append(TestCase(f"test_{function_name}_example_{index + 1}", "success", item["input"], item["expected"]))
    for index, expression in enumerate(invalid_inputs or []):
        if not isinstance(expression, str) or not expression.strip():
            raise ValueError("invalid input expressions must be non-empty strings")
        cases.append(TestCase(f"test_{function_name}_invalid_{index + 1}", "error", expression, None))
    return cases


def render_pytest(function_name: str, cases: list[TestCase]) -> str:
    lines = ["import pytest", "", f"from app.module import {function_name}", ""]
    for case in cases:
        lines.append(f"def {case.name}():")
        if case.category == "success":
            lines.append(f"    assert {function_name}({case.input_expression}) == {case.expected_expression}")
        else:
            lines.append(f"    with pytest.raises((TypeError, ValueError)):")
            lines.append(f"        {function_name}({case.input_expression})")
        lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    print(render_pytest("double", generate_cases("double", [{"input": "2", "expected": "4"}])))
