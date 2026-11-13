import pytest

from app.reproduction import build_plan, to_json


def test_extracts_reported_facts_without_fabricating_steps():
    plan = build_plan("API fails with timeout\nPython 3.12 on Ubuntu 24.04")
    assert plan.reported_environment == ("Python 3.12 on Ubuntu 24.04",)
    assert plan.reported_symptoms == ("API fails with timeout",)
    assert plan.reproduction_steps == ()
    assert any("sequence" in item for item in plan.missing_information)


def test_accepts_explicit_steps_and_serializes():
    plan = build_plan("Crash on upload", ["1. Sign in", "2. Upload a file"])
    assert len(plan.reproduction_steps) == 2
    assert '"reproduction_steps"' in to_json(plan)


def test_rejects_empty_report():
    with pytest.raises(ValueError):
        build_plan("  ")
