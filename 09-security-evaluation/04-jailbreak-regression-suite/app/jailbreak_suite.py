"""Jailbreak regression suite: deterministic security evaluation helpers."""

def run_regression_suite(*, cases: list[dict[str, object]], response_validator):
    if not callable(response_validator):
        raise TypeError("response_validator must be callable")
    results = []
    for case in cases:
        if not isinstance(case, dict) or not isinstance(case.get("name"), str) or not isinstance(case.get("response"), str):
            raise ValueError("each case requires name and response strings")
        expected = bool(case.get("expected_safe", True))
        actual = bool(response_validator(case["response"]))
        results.append({"name": case["name"], "expected_safe": expected, "actual_safe": actual, "passed": actual == expected})
    return {"passed": sum(x["passed"] for x in results), "failed": sum(not x["passed"] for x in results), "results": results}
