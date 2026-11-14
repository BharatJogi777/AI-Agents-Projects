"""Extract structured methodology fields from supplied text without inference."""
from dataclasses import dataclass
@dataclass(frozen=True)
class Methodology:
    study_design: str
    population: str
    sample_size: int | None
    intervention: str
    outcome_measures: tuple[str,...]
    analysis_method: str
    unreported_fields: tuple[str,...]
def extract_methodology(*, study_design: str="", population: str="", sample_size: int|None=None, intervention: str="", outcome_measures: list[str]|None=None, analysis_method: str="") -> Methodology:
    fields={"study_design":study_design,"population":population,"intervention":intervention,"analysis_method":analysis_method}
    if any(not isinstance(v,str) for v in fields.values()): raise ValueError("text fields must be strings")
    if sample_size is not None and (not isinstance(sample_size,int) or isinstance(sample_size,bool) or sample_size<1): raise ValueError("sample_size must be a positive integer or None")
    measures=[] if outcome_measures is None else outcome_measures
    if not isinstance(measures,list) or any(not isinstance(v,str) or not v.strip() for v in measures): raise ValueError("outcome_measures must be a list of non-empty strings")
    missing=tuple(k for k,v in fields.items() if not v.strip())+tuple(["sample_size"] if sample_size is None else [])+tuple(["outcome_measures"] if not measures else [])
    return Methodology(study_design.strip(),population.strip(),sample_size,intervention.strip(),tuple(v.strip() for v in measures),analysis_method.strip(),missing)
