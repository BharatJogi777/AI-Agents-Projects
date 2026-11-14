"""Compare supplied competitor snapshots without performing web collection."""
from dataclasses import dataclass
@dataclass(frozen=True)
class FieldChange:
    entity_id: str
    field: str
    previous: object
    current: object
@dataclass(frozen=True)
class SnapshotDiff:
    added_entities: tuple[str,...]
    removed_entities: tuple[str,...]
    changed_fields: tuple[FieldChange,...]
def compare_snapshots(*, previous: list[dict], current: list[dict], id_field: str="entity_id") -> SnapshotDiff:
    if not isinstance(id_field,str) or not id_field.strip(): raise ValueError("id_field must be non-empty")
    def index(rows):
        if not isinstance(rows,list): raise ValueError("snapshots must be lists")
        result={}
        for row in rows:
            if not isinstance(row,dict) or not isinstance(row.get(id_field),str) or not row[id_field].strip(): raise ValueError(f"each entity needs a non-empty {id_field}")
            key=row[id_field].strip()
            if key in result: raise ValueError(f"duplicate entity ID: {key}")
            result[key]=row
        return result
    old=index(previous); new=index(current)
    added=tuple(sorted(new.keys()-old.keys())); removed=tuple(sorted(old.keys()-new.keys()))
    changes=[]
    for entity in sorted(old.keys()&new.keys()):
        for field in sorted((old[entity].keys()|new[entity].keys())-{id_field}):
            before=old[entity].get(field); after=new[entity].get(field)
            if before!=after: changes.append(FieldChange(entity,field,before,after))
    return SnapshotDiff(added,removed,tuple(changes))
