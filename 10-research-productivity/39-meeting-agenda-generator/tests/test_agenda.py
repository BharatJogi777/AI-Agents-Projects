from app.agenda import AgendaItem, generate_agenda
import pytest

def test_agenda_has_offsets_and_outcomes():
    result=generate_agenda("Decide launch", [AgendaItem("Risks",10,"Risk list"),AgendaItem("Plan",15,"Owners")],30)
    assert result[1]["start_minute"] == 10
    assert result[0]["desired_outcome"] == "Risk list"

def test_overflow_rejected():
    with pytest.raises(ValueError, match="requires"):
        generate_agenda("Decide", [AgendaItem("Topic",20,"Outcome")],10)

def test_missing_objective_rejected():
    with pytest.raises(ValueError):
        generate_agenda("", [AgendaItem("Topic",1,"Outcome")],10)
