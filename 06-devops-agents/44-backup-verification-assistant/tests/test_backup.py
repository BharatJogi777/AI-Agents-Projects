from app.backup import verify_backups
import pytest

def test_flags_stale_backup_and_missing_integrity():
    result=verify_backups([{"backup_id":"b1","age_hours":48,"last_restore_test_days":120,"integrity_verified":False,"coverage_complete":True}])
    assert result[0].status=="attention_required" and len(result[0].issues)==3

def test_rejects_duplicate_backup_ids():
    item={"backup_id":"b","age_hours":1,"last_restore_test_days":1,"integrity_verified":True,"coverage_complete":True}
    with pytest.raises(ValueError): verify_backups([item,item])
