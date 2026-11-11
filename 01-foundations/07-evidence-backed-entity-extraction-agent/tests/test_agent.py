import json

import pytest

from app.agent import EvidenceBackedEntityExtractor, ExtractionValidationError
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
        {"value": "Bharat", "entity_type": "person", "evidence": "Bharat deployed the Checkout API"},
        {"value": "Checkout API", "entity_type": "service", "evidence": "deployed the Checkout API in Bengaluru"},
        {"value": "Bengaluru", "entity_type": "location", "evidence": "in Bengaluru on 12 November 2026"},
        {"value": "12 November 2026", "entity_type": "date_or_time", "evidence": "on 12 November 2026."},
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
    result = EvidenceBackedEntityExtractor(FakeGenerator('{"entities": []}')).extract("No named entities.")
    assert result.entities == []


def test_invalid_json_and_unknown_entity_type_are_rejected():
    with pytest.raises(ExtractionValidationError):
        EvidenceBackedEntityExtractor(FakeGenerator("{not-json")).extract(SOURCE)
    payload = json.loads(VALID)
    payload["entities"][0]["entity_type"] = "planet"
    with pytest.raises(ExtractionValidationError):
        EvidenceBackedEntityExtractor(FakeGenerator(json.dumps(payload))).extract(SOURCE)


def test_unknown_fields_and_duplicate_entities_are_rejected():
    payload = json.loads(VALID)
    payload["surprise"] = True
    with pytest.raises(ExtractionValidationError):
        EvidenceBackedEntityExtractor(FakeGenerator(json.dumps(payload))).extract(SOURCE)
    payload = json.loads(VALID)
    payload["entities"].append(payload["entities"][0])
    with pytest.raises(ExtractionValidationError):
        EvidenceBackedEntityExtractor(FakeGenerator(json.dumps(payload))).extract(SOURCE)


def test_evidence_must_be_exact_and_contain_entity_value():
    payload = json.loads(VALID)
    payload["entities"][0]["evidence"] = "Bharat worked on the API"
    with pytest.raises(ExtractionValidationError, match="exact source substring"):
        EvidenceBackedEntityExtractor(FakeGenerator(json.dumps(payload))).extract(SOURCE)
    payload = json.loads(VALID)
    payload["entities"][0]["value"] = "Bharat Jogi"
    with pytest.raises(ExtractionValidationError, match="does not appear"):
        EvidenceBackedEntityExtractor(FakeGenerator(json.dumps(payload))).extract(SOURCE)


def test_input_and_output_byte_limits_are_enforced():
    generator = FakeGenerator(VALID)
    extractor = EvidenceBackedEntityExtractor(generator, max_input_bytes=8)
    with pytest.raises(ValueError, match="byte limit"):
        extractor.extract("long enough")
    assert generator.messages is None
    with pytest.raises(ExtractionValidationError, match="byte limit"):
        EvidenceBackedEntityExtractor(FakeGenerator(VALID), max_output_bytes=10).extract(SOURCE)
