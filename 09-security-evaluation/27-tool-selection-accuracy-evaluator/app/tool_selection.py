"""Measure whether selected tools match a reference tool set."""
from dataclasses import dataclass

@dataclass(frozen=True)
class SelectionMetrics:
    precision: float
    recall: float
    f1: float
    false_positives: tuple[str,...]
    false_negatives: tuple[str,...]

def evaluate_selection(selected: set[str], expected: set[str]) -> SelectionMetrics:
    if not isinstance(selected,set) or not isinstance(expected,set): raise ValueError("inputs must be sets")
    if any(not isinstance(x,str) or not x for x in selected | expected): raise ValueError("tool names must be non-empty strings")
    tp=selected & expected; fp=selected-expected; fn=expected-selected
    precision=len(tp)/len(selected) if selected else (1.0 if not expected else 0.0)
    recall=len(tp)/len(expected) if expected else (1.0 if not selected else 0.0)
    f1=2*precision*recall/(precision+recall) if precision+recall else 0.0
    return SelectionMetrics(precision,recall,f1,tuple(sorted(fp)),tuple(sorted(fn)))
