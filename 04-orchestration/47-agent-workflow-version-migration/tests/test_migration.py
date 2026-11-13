import pytest
from app.migration import MigrationRegistry

def test_sequential_migrations():
    r=MigrationRegistry({(1,2):lambda s:{**s,"b":2},(2,3):lambda s:{**s,"c":3}})
    assert r.migrate({"a":1},1,3) == {"a":1,"b":2,"c":3}

def test_missing_and_bad_migration():
    with pytest.raises(LookupError): MigrationRegistry({}).migrate({},1,2)
    with pytest.raises(TypeError): MigrationRegistry({(1,2):lambda s:None}).migrate({},1,2)
