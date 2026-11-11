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
        {"task": "Inspect API latency metrics and recent deployments", "owner": None, "due_date": None}
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
    generator = FakeGenerator("{not-json")

    with pytest.raises(OutputValidationError, match="did not satisfy"):
        StructuredOutputAgent(generator).analyze("Classify this request")


def test_invalid_enum_is_rejected():
    payload = json.loads(VALID_OUTPUT)
    payload["priority"] = "urgent-ish"

    with pytest.raises(OutputValidationError):
        StructuredOutputAgent(FakeGenerator(json.dumps(payload))).analyze("Classify this request")


def test_unknown_fields_are_rejected():
    payload = json.loads(VALID_OUTPUT)
    payload["made_up_field"] = "not allowed"

    with pytest.raises(OutputValidationError):
        StructuredOutputAgent(FakeGenerator(json.dumps(payload))).analyze("Classify this request")


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
