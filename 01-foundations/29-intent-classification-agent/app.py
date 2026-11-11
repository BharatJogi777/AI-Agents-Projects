"""Backward-compatible facade; use intent_classifier for new code."""
from intent_classifier import IntentClassifier,IntentResult
__all__=["IntentClassifier","IntentResult"]
