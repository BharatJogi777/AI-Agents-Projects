import json

import pytest

from app.agent import SchemaRepairAgent, SchemaRepairExhausted
from app.schemas import Priority, TaskReport


VALID = json.dumps({
    "summary": "Investigate elevated checkout API latency.",
    "priority": "high",
    "action_items": [{"task": "Inspect API latency metrics", "owner": None}],
    "needs_human_review": True,
})


class SequenceGenerator:
    def __init__(self, outputs):
        self.outputs = list(outputs)
        self.calls = []

    def generate_structured(self, messages, json_schema):
        self.calls.append((messages, json_schema))
        item = self.outputs.pop(0)
        if isinstance(item, Exception):
            raise item
        return item


def test_valid_first_response_needs_no_repair():
    generator = SequenceGenerator([VALID])
    result = SchemaRepairAgent(generator).generate("Checkout latency increased.")

    assert isinstance(result.report, TaskReport)
    assert result.report.priority is Priority.HIGH
    assert (result.attempts, result.repairs) == (1, 0)
    assert len(generator.calls) == 1


def test_invalid_json_is_repaired_on_second_attempt():
    generator = SequenceGenerator(["{broken-json", VALID])
    result = SchemaRepairAgent(generator).generate("Checkout latency increased.")

    assert result.report.priority is Priority.HIGH
    assert (result.attempts, result.repairs) == (2, 1)
    repair_messages = generator.calls[1][0]
    assert repair_messages[-1]["role"] == "user"
    assert "Validation feedback" in repair_messages[-1]["content"]


def test_schema_error_is_sent_as_feedback_without_echoing_input_values():
    bad = json.dumps({
        "summary": "tiny",
        "priority": "urgent",
        "action_items": [],
        "needs_human_review": False,
    })
    generator = SequenceGenerator([bad, VALID])
    result = SchemaRepairAgent(generator).generate("private request content")
    feedback = generator.calls[1][0][-1]["content"]

    assert result.repairs == 1
    assert "summary" in feedback
    assert "priority" in feedback
    assert "private request content" not in feedback


def test_retries_stop_at_configured_limit():
    generator = SequenceGenerator(["not-json", "still-not-json", VALID])
    agent = SchemaRepairAgent(generator, max_retries=1)

    with pytest.raises(SchemaRepairExhausted) as error:
        agent.generate("Do work")

    assert error.value.attempts == 2
    assert len(generator.calls) == 2


def test_zero_retries_means_exactly_one_attempt():
    generator = SequenceGenerator(["not-json", VALID])
    with pytest.raises(SchemaRepairExhausted):
        SchemaRepairAgent(generator, max_retries=0).generate("Do work")
    assert len(generator.calls) == 1


def test_empty_model_response_can_be_retried():
    generator = SequenceGenerator(["  ", VALID])
    result = SchemaRepairAgent(generator).generate("Do work")
    assert result.repairs == 1


def test_oversized_model_output_is_rejected_and_retried():
    generator = SequenceGenerator(["x" * 101, VALID])
    result = SchemaRepairAgent(
        generator, max_output_chars=100
    ).generate("Do work")
    assert result.attempts == 2


def test_transport_failure_is_not_retried_as_schema_failure():
    generator = SequenceGenerator([RuntimeError("connection failed"), VALID])
    with pytest.raises(RuntimeError, match="connection failed"):
        SchemaRepairAgent(generator).generate("Do work")
    assert len(generator.calls) == 1


def test_retry_configuration_is_bounded():
    with pytest.raises(ValueError, match="max_retries"):
        SchemaRepairAgent(SequenceGenerator([]), max_retries=4)
    with pytest.raises(ValueError, match="max_output_chars"):
        SchemaRepairAgent(SequenceGenerator([]), max_output_chars=10)


def test_empty_and_oversized_requests_are_rejected_before_model_call():
    generator = SequenceGenerator([VALID])
    agent = SchemaRepairAgent(generator)
    with pytest.raises(ValueError, match="cannot be empty"):
        agent.generate(" ")
    with pytest.raises(ValueError, match="20000-character"):
        agent.generate("x" * 20_001)
    assert generator.calls == []


def test_unknown_fields_are_rejected_then_can_be_repaired():
    payload = json.loads(VALID)
    payload["surprise"] = "not allowed"
    generator = SequenceGenerator([json.dumps(payload), VALID])
    result = SchemaRepairAgent(generator).generate("Do work")
    assert result.repairs == 1
