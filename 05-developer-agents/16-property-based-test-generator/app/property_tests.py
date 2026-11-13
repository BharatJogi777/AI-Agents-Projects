"""Render property-based test ideas from explicit domains and invariants."""
from __future__ import annotations
from dataclasses import asdict, dataclass
import json
import keyword


@dataclass(frozen=True)
class Property:
    name: str
    domain: str
    invariant: str
    example_strategy: str


def generate_properties(function_name: str, domains: dict[str, str], invariants: list[str]) -> list[Property]:
    if not isinstance(function_name, str) or not function_name.isidentifier() or keyword.iskeyword(function_name):
        raise ValueError("function_name must be a Python identifier")
    if not isinstance(domains, dict) or any(not isinstance(k, str) or not k.isidentifier() or not isinstance(v, str) or not v.strip() for k, v in domains.items()):
        raise ValueError("domains must map valid parameter names to non-empty descriptions")
    if not isinstance(invariants, list) or any(not isinstance(x, str) or not x.strip() for x in invariants):
        raise ValueError("invariants must be a list of non-empty strings")
    if not invariants:
        raise ValueError("at least one invariant is required")
    joined = ", ".join(f"{key}={value}" for key, value in domains.items()) or "no parameters specified"
    return [Property(f"test_{function_name}_property_{i+1}", joined, invariant.strip(),
                     "hypothesis.strategies.integers()  # replace with domain-specific strategies")
            for i, invariant in enumerate(invariants)]


def render_pytest(function_name: str, properties: list[Property]) -> str:
    lines = ["# Review and adapt these generated property specifications.", "from hypothesis import given, strategies as st",
             f"from app.module import {function_name}", ""]
    for item in properties:
        lines.extend([f"# Domain: {item.domain}", f"# Invariant: {item.invariant}",
                      f"def {item.name}():", "    # Replace this placeholder with a domain-specific @given strategy.",
                      "    raise NotImplementedError('Complete the property before enabling it')", ""])
    return "\n".join(lines)


def to_json(properties: list[Property]) -> str:
    return json.dumps([asdict(item) for item in properties], indent=2)


if __name__ == "__main__":
    print(to_json(generate_properties("normalize", {"value": "arbitrary string"}, ["normalization is idempotent"])))
