"""Identify unaddressed dimensions in a caller-defined research matrix."""
from dataclasses import dataclass
@dataclass(frozen=True)
class ResearchGaps:
    covered_dimensions: tuple[str,...]
    missing_dimensions: tuple[str,...]
    coverage_ratio: float
def find_research_gaps(*, required_dimensions: list[str], observed_dimensions: list[str]) -> ResearchGaps:
    for name, values in (("required_dimensions",required_dimensions),("observed_dimensions",observed_dimensions)):
        if not isinstance(values,list) or any(not isinstance(v,str) or not v.strip() for v in values): raise ValueError(f"{name} must be a list of non-empty strings")
    required=set(required_dimensions); observed=set(observed_dimensions)
    if not required: raise ValueError("at least one required dimension is needed")
    covered=tuple(sorted(required&observed)); missing=tuple(sorted(required-observed))
    return ResearchGaps(covered,missing,len(covered)/len(required))
