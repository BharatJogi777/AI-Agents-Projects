from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, model_validator


class EntityType(StrEnum):
    PERSON = "person"
    ORGANIZATION = "organization"
    PRODUCT = "product"
    SERVICE = "service"
    LOCATION = "location"
    DATE_OR_TIME = "date_or_time"
    IDENTIFIER = "identifier"


class ExtractedEntity(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    value: str = Field(min_length=1, max_length=200)
    entity_type: EntityType
    evidence: str = Field(min_length=1, max_length=500)


class ExtractionResult(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    entities: list[ExtractedEntity] = Field(max_length=100)

    @model_validator(mode="after")
    def reject_duplicate_entities(self):
        keys = [(entity.entity_type, entity.value.casefold()) for entity in self.entities]
        if len(keys) != len(set(keys)):
            raise ValueError("duplicate entities are not allowed")
        return self
