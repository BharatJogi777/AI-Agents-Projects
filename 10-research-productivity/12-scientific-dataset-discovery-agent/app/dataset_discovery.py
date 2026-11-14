"""Filter a supplied scientific dataset catalogue; performs no external discovery."""
from dataclasses import dataclass
@dataclass(frozen=True)
class DatasetMatch:
    dataset_id: str
    matched_fields: tuple[str,...]
    missing_requirements: tuple[str,...]
def discover_datasets(*, catalogue: list[dict], required_topics: list[str], required_formats: list[str]=[]) -> tuple[DatasetMatch,...]:
    if not isinstance(catalogue,list) or not isinstance(required_topics,list) or not isinstance(required_formats,list): raise ValueError("catalogue and requirements must be lists")
    if any(not isinstance(x,str) or not x.strip() for x in required_topics+required_formats): raise ValueError("requirements must be non-empty strings")
    results=[]
    for item in catalogue:
        if not isinstance(item,dict) or not isinstance(item.get("dataset_id"),str) or not item["dataset_id"].strip(): raise ValueError("each dataset needs a dataset_id")
        topics=item.get("topics",[]); formats=item.get("formats",[])
        if not isinstance(topics,list) or not isinstance(formats,list): raise ValueError("topics and formats must be lists")
        normalized={str(x).casefold() for x in topics+formats}
        missing=tuple(x for x in required_topics+required_formats if x.casefold() not in normalized)
        matched=tuple(x for x in required_topics+required_formats if x.casefold() in normalized)
        if not missing: results.append(DatasetMatch(item["dataset_id"],matched,()))
    return tuple(results)
