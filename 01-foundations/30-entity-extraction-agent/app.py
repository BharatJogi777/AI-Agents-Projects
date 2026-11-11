"""Backward-compatible facade; use entity_extractor for new code."""
from entity_extractor import Entity,EntityExtractionError,EntityExtractor
__all__=["Entity","EntityExtractionError","EntityExtractor"]
