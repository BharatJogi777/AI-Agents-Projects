import pytest
from app.upgrade import plan_upgrades, to_json


def test_classifies_upgrade_types():
    result = plan_upgrades({"a": "1.2.3", "b": "1.2.3", "c": "1.2.3"},
                           {"a": "2.0.0", "b": "1.3.0", "c": "1.2.4"})
    assert [x.change_type for x in result] == ["major", "minor", "patch"]
    assert '"rollback"' in to_json(result)[0:]


def test_detects_downgrade_and_unchanged():
    result = plan_upgrades({"a": "2.0.0", "b": "1.0.0"}, {"a": "1.9.9", "b": "1.0.0"})
    assert [x.change_type for x in result] == ["downgrade", "unchanged"]


def test_rejects_missing_package_and_bad_version():
    with pytest.raises(ValueError):
        plan_upgrades({}, {"x": "1.0.0"})
    with pytest.raises(ValueError):
        plan_upgrades({"x": "latest"}, {"x": "1.0.0"})
