import pytest
from app.competitor_monitor import compare_snapshots
def test_detects_added_removed_and_changed_entities():
 r=compare_snapshots(previous=[{"entity_id":"A","price":10},{"entity_id":"B"}],current=[{"entity_id":"A","price":12},{"entity_id":"C"}])
 assert r.added_entities==("C",) and r.removed_entities==("B",)
 assert [(x.entity_id,x.field,x.previous,x.current) for x in r.changed_fields]==[("A","price",10,12)]
def test_rejects_duplicate_ids():
 with pytest.raises(ValueError):
  compare_snapshots(previous=[{"entity_id":"A"},{"entity_id":"A"}],current=[])
def test_detects_new_and_removed_fields():
 r=compare_snapshots(previous=[{"entity_id":"A","old":"x"}],current=[{"entity_id":"A","new":"y"}])
 assert {(x.field,x.previous,x.current) for x in r.changed_fields}=={("old","x",None),("new",None,"y")}
