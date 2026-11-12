import json

import pytest

from app.agent import OutputValidationError, StructuredOutputAgent
from app.schemas import Category, Priority, TaskAnalysis


class FakeGenerator:
    def __init__(self, output: str):
        self.output = output
        self.messages = None
        self.schema = None

    def generate_structured(self, messages, json_schema):
        self.messages = messages
        self.schema = json_schema
        return self.output


VALID_OUTPUT = json.dumps({
    "summary": "Investigate elevated API latency affecting checkout requests.",
    "priority": "high",
    "category": "operations",
    "action_items": [
        {
            "task": "Inspect API latency metrics and recent deployments",
            "evidence": "Checkout API latency increased.",
            "owner": None,
            "owner_evidence": None,
            "due_date": None,
            "due_date_evidence": None,
        }
    ],
    "needs_human_review": True,
    "uncertainty": "The affected time window and customer impact are not specified.",
})


def test_valid_json_is_parsed_into_typed_pydantic_model():
    generator = FakeGenerator(VALID_OUTPUT)
    result = StructuredOutputAgent(generator).analyze("Checkout API latency increased.")

    assert isinstance(result, TaskAnalysis)
    assert result.priority is Priority.HIGH
    assert result.category is Category.OPERATIONS
    assert result.action_items[0].owner is None
    assert generator.schema["type"] == "object"
    assert generator.messages[0]["role"] == "system"


def test_invalid_json_is_rejected():
    with pytest.raises(OutputValidationError, match="did not satisfy"):
        StructuredOutputAgent(FakeGenerator("{not-json")).analyze("Classify this request")


def test_invalid_enum_is_rejected():
    payload = json.loads(VALID_OUTPUT)
    payload["priority"] = "urgent-ish"
    with pytest.raises(OutputValidationError):
        StructuredOutputAgent(FakeGenerator(json.dumps(payload))).analyze("Checkout API latency increased.")


def test_unknown_fields_are_rejected():
    payload = json.loads(VALID_OUTPUT)
    payload["made_up_field"] = "not allowed"
    with pytest.raises(OutputValidationError):
        StructuredOutputAgent(FakeGenerator(json.dumps(payload))).analyze("Checkout API latency increased.")


def test_empty_input_is_rejected_before_model_call():
    generator = FakeGenerator(VALID_OUTPUT)
    with pytest.raises(ValueError, match="cannot be empty"):
        StructuredOutputAgent(generator).analyze(" ")
    assert generator.messages is None


def test_schema_contract_has_required_fields():
    schema = TaskAnalysis.model_json_schema()
    assert {"summary", "priority", "category", "action_items", "needs_human_review"} <= set(
        schema["properties"]
    )
    action_schema = schema["$defs"]["ActionItem"]
    assert "evidence" in action_schema["properties"]


def test_input_size_is_bounded_before_model_call():
    generator = FakeGenerator(VALID_OUTPUT)
    with pytest.raises(ValueError, match="size limit"):
        StructuredOutputAgent(generator, max_input_bytes=10).analyze("x" * 11)
    assert generator.messages is None


def test_oversized_model_output_is_rejected_before_json_parsing():
    with pytest.raises(OutputValidationError, match="size limit"):
        StructuredOutputAgent(FakeGenerator("x" * 100), max_output_bytes=50).analyze("Classify this request")


def test_non_text_model_output_is_rejected():
    with pytest.raises(OutputValidationError, match="not text"):
        StructuredOutputAgent(FakeGenerator(None)).analyze("Classify this request")


def test_fabricated_evidence_quote_is_rejected():
    payload = json.loads(VALID_OUTPUT)
    payload["action_items"][0]["evidence"] = "The database is corrupted."
    with pytest.raises(OutputValidationError, match="not an exact source substring"):
        StructuredOutputAgent(FakeGenerator(json.dumps(payload))).analyze("Checkout API latency increased.")


def test_owner_without_owner_evidence_is_rejected_by_schema():
    payload = json.loads(VALID_OUTPUT)
    payload["action_items"][0]["owner"] = "Alice"
    with pytest.raises(OutputValidationError, match="did not satisfy"):
        StructuredOutputAgent(FakeGenerator(json.dumps(payload))).analyze("Checkout API latency increased.")


def test_owner_must_appear_in_exact_source_evidence():
    payload = json.loads(VALID_OUTPUT)
    payload["action_items"][0]["owner"] = "Alice"
    payload["action_items"][0]["owner_evidence"] = "The task is assigned to Alice."
    with pytest.raises(OutputValidationError, match="owner is not supported"):
        StructuredOutputAgent(FakeGenerator(json.dumps(payload))).analyze("Checkout API latency increased.")


def test_explicit_owner_with_matching_evidence_is_accepted():
    payload = json.loads(VALID_OUTPUT)
    payload["action_items"][0]["owner"] = "Alice"
    payload["action_items"][0]["owner_evidence"] = "Alice will inspect the metrics."
    result = StructuredOutputAgent(FakeGenerator(json.dumps(payload))).analyze(
        "Checkout API latency increased. Alice will inspect the metrics."
    )
    assert result.action_items[0].owner == "Alice"

def test_due_date_requires_matching_source_evidence():
    payload = json.loads(VALID_OUTPUT)
    payload["action_items"][0]["due_date"] = "2026-11-15"
    payload["action_items"][0]["due_date_evidence"] = "The deadline is 2026-11-15."
    with pytest.raises(OutputValidationError, match="due date is not supported"):
        StructuredOutputAgent(FakeGenerator(json.dumps(payload))).analyze(
            "Checkout API latency increased. Alice will inspect the metrics."
        )


def test_explicit_due_date_with_matching_evidence_is_accepted():
    payload = json.loads(VALID_OUTPUT)
    payload["action_items"][0]["due_date"] = "2026-11-15"
    payload["action_items"][0]["due_date_evidence"] = "Complete by 2026-11-15."
    result = StructuredOutputAgent(FakeGenerator(json.dumps(payload))).analyze(
        "Checkout API latency increased. Complete by 2026-11-15."
    )
    assert result.action_items[0].due_date == "2026-11-15"
