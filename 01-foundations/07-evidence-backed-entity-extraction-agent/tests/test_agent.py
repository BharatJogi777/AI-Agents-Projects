import json

import pytest

from app.agent import (
    EvidenceBackedEntityExtractor,
    ExtractionValidationError,
)
from app.schemas import EntityType, ExtractionResult


class FakeGenerator:
    def __init__(self, output: str):
        self.output = output
        self.messages = None
        self.schema = None

    def generate_structured(self, messages, json_schema):
        self.messages = messages
        self.schema = json_schema
        return self.output


SOURCE = "Bharat deployed the Checkout API in Bengaluru on 12 November 2026."
VALID = json.dumps({
    "entities": [
        {
            "value": "Bharat",
            "entity_type": "person",
            "evidence": "Bharat deployed the Checkout API",
        },
        {
            "value": "Checkout API",
            "entity_type": "service",
            "evidence": "deployed the Checkout API in Bengaluru",
        },
        {
            "value": "Bengaluru",
            "entity_type": "location",
            "evidence": "in Bengaluru on 12 November 2026",
        },
        {
            "value": "12 November 2026",
            "entity_type": "date_or_time",
            "evidence": "on 12 November 2026.",
        },
    ]
})


def test_extracts_typed_entities_with_exact_evidence():
    generator = FakeGenerator(VALID)
    result = EvidenceBackedEntityExtractor(generator).extract(SOURCE)

    assert isinstance(result, ExtractionResult)
    assert len(result.entities) == 4
    assert result.entities[0].entity_type is EntityType.PERSON
    assert generator.schema["type"] == "object"
    assert generator.messages[0]["role"] == "system"


def test_empty_entity_list_is_valid():
    result = EvidenceBackedEntityExtractor(
        FakeGenerator('{"entities": []}')
    ).extract("No named entities appear here.")
    assert result.entities == []


def test_invalid_json_is_rejected():
    with pytest.raises(ExtractionValidationError, match="schema"):
        EvidenceBackedEntityExtractor(FakeGenerator("{not-json")).extract(SOURCE)


def test_unknown_entity_type_is_rejected():
    payload = json.loads(VALID)
    payload["entities"][0]["entity_type"] = "planet"
    with pytest.raises(ExtractionValidationError):
        EvidenceBackedEntityExtractor(FakeGenerator(json.dumps(payload))).extract(SOURCE)


def test_unknown_fields_are_rejected():
    payload = json.loads(VALID)
    payload["unexpected"] = "value"
    with pytest.raises(ExtractionValidationError):
        EvidenceBackedEntityExtractor(FakeGenerator(json.dumps(payload))).extract(SOURCE)


def test_evidence_must_be_an_exact_source_substring():
    payload = json.loads(VALID)
    payload["entities"][0]["evidence"] = "Bharat worked on the API"
    with pytest.raises(ExtractionValidationError, match="exact source substring"):
        EvidenceBackedEntityExtractor(FakeGenerator(json.dumps(payload))).extract(SOURCE)


def test_entity_value_must_appear_in_its_evidence():
    payload = json.loads(VALID)
    payload["entities"][0]["value"] = "Bharat Jogi"
    with pytest.raises(ExtractionValidationError, match="does not appear"):
        EvidenceBackedEntityExtractor(FakeGenerator(json.dumps(payload))).extract(SOURCE)


def test_duplicate_entities_are_rejected():
    payload = json.loads(VALID)
    payload["entities"].append(payload["entities"][0])
    with pytest.raises(ExtractionValidationError):
        EvidenceBackedEntityExtractor(FakeGenerator(json.dumps(payload))).extract(SOURCE)


def test_empty_and_oversized_inputs_are_rejected_before_model_call():
    generator = FakeGenerator(VALID)
    extractor = EvidenceBackedEntityExtractor(generator)
    with pytest.raises(ValueError, match="cannot be empty"):
        extractor.extract(" ")
    with pytest.raises(ValueError, match="20000-character"):
        extractor.extract("x" * 20_001)
    assert generator.messages is None


def test_schema_contract_is_strict():
    schema = ExtractionResult.model_json_schema()
    assert schema["additionalProperties"] is False
    assert "entities" in schema["properties"]
