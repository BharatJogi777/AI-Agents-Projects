import pytest
from app.research import FanOutFanIn, ResearchFinding

def researcher(question):
    if question == "broken": raise RuntimeError("source unavailable")
    return ResearchFinding(question, "evidence-based answer", ("source://1",))

def test_fan_out_fan_in_collects_results_and_errors():
    report = FanOutFanIn(researcher, 2).run(["one", "broken", "two"])
    assert [f.question for f in report.findings] == ["one", "two"]
    assert report.failures == {"broken": "source unavailable"}

def test_duplicate_questions_rejected():
    with pytest.raises(ValueError):
        FanOutFanIn(researcher).run(["same", "same"])

def test_mismatched_finding_rejected():
    workflow = FanOutFanIn(lambda q: ResearchFinding("other", "x"))
    report = workflow.run(["requested"])
    assert "requested" in report.failures
