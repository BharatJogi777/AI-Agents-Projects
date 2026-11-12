import pytest

from calculator_core.arithmetic import CalculationError, calculate


@pytest.mark.parametrize("expression", [
    "1e101",
    "1e100 * 1e100",
    "1e-100 ** -8",
    "1 / (2 - 2)",
    "1e100 ** 8",
])
def test_out_of_range_or_undefined_results_fail_closed(expression):
    with pytest.raises(CalculationError):
        calculate(expression)


def test_decimal_precision_is_deterministic():
    assert calculate("1 / 3") == "0.3333333333333333333333333333"


def test_ast_node_budget_is_enforced():
    expression = "+".join(["1"] * 25)
    with pytest.raises(CalculationError, match="too complex"):
        calculate(expression)


def test_attribute_and_container_access_are_rejected():
    for expression in ["(1).__class__", "(1, 2)[0]", "1 if 1 else 2"]:
        with pytest.raises(CalculationError):
            calculate(expression)


def test_small_finite_decimal_result_is_supported():
    result = calculate("1e-100 ** 8")
    assert result.startswith("0.")
    assert len(result) > 700
