"""Critique hypothesis quality using explicit research-design criteria."""
from dataclasses import dataclass
@dataclass(frozen=True)
class HypothesisCritique:
    score: int
    strengths: tuple[str,...]
    improvements: tuple[str,...]
    review_required: bool = True
def critique_hypothesis(*, hypothesis: str, population: str, variables: list[str], measurable_outcome: str, falsifiable_condition: str) -> HypothesisCritique:
    vals={"hypothesis":hypothesis,"population":population,"measurable_outcome":measurable_outcome,"falsifiable_condition":falsifiable_condition}
    if any(not isinstance(v,str) for v in vals.values()): raise ValueError("text fields must be strings")
    if not isinstance(variables,list) or any(not isinstance(v,str) or not v.strip() for v in variables): raise ValueError("variables must be non-empty strings")
    checks=[bool(hypothesis.strip()),bool(population.strip()),len(set(variables))>=2,bool(measurable_outcome.strip()),bool(falsifiable_condition.strip())]
    labels=("hypothesis is stated","target population is specified","at least two distinct variables are specified","outcome is measurable","a falsifiable condition is described")
    strengths=tuple(x for x,ok in zip(labels,checks) if ok)
    improvements=tuple(f"Specify {x}" for x,ok in zip(("a clear hypothesis","the target population","distinct independent and dependent variables","a measurable outcome","a falsifiable condition"),checks) if not ok)
    return HypothesisCritique(round(sum(checks)/len(checks)*100),strengths,improvements)
