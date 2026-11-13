import pytest
from app.backup import verify_backups

def test_flags_stale_unencrypted_backup():
 r=verify_backups([{'backup_id':'b1','age_hours':48,'last_restore_test_days':120,'integrity_check_passed':True,'encrypted':False}])
 assert r[0].status=='attention_required' and len(r[0].issues)==3

def test_rejects_duplicate_ids():
 x={'backup_id':'b','age_hours':1,'last_restore_test_days':1,'integrity_check_passed':True,'encrypted':True}
 with pytest.raises(ValueError): verify_backups([x,x])
