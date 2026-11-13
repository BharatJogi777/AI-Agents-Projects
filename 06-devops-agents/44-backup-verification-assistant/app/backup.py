"""Assess backup evidence; metadata checks do not prove recoverability."""
from dataclasses import dataclass

@dataclass(frozen=True)
class BackupFinding:
    backup_id: str
    status: str
    issues: tuple[str,...]

def verify_backups(records: list[dict], *, max_age_hours: float=24, max_restore_test_age_days: int=90) -> list[BackupFinding]:
    if not isinstance(records,list): raise TypeError("records must be a list")
    if isinstance(max_age_hours,bool) or not isinstance(max_age_hours,(int,float)) or max_age_hours<=0: raise ValueError("max_age_hours must be positive")
    if isinstance(max_restore_test_age_days,bool) or not isinstance(max_restore_test_age_days,int) or max_restore_test_age_days<0: raise ValueError("max_restore_test_age_days must be non-negative")
    out=[]; seen=set()
    for i,r in enumerate(records):
        if not isinstance(r,dict): raise ValueError(f"record {i} must be an object")
        bid=r.get("backup_id"); age=r.get("age_hours"); restore_age=r.get("last_restore_test_days"); integrity=r.get("integrity_verified"); covered=r.get("coverage_complete")
        if not isinstance(bid,str) or not bid or bid in seen: raise ValueError("backup_id must be unique and non-empty")
        seen.add(bid); issues=[]
        if isinstance(age,bool) or not isinstance(age,(int,float)) or age<0: raise ValueError(f"{bid}: invalid age_hours")
        if isinstance(restore_age,bool) or not isinstance(restore_age,int) or restore_age<0: raise ValueError(f"{bid}: invalid last_restore_test_days")
        if not isinstance(integrity,bool) or not isinstance(covered,bool): raise ValueError(f"{bid}: verification flags must be booleans")
        if age>max_age_hours: issues.append("Backup is stale.")
        if not integrity: issues.append("Integrity verification is missing or failed.")
        if not covered: issues.append("Expected backup coverage is incomplete.")
        if restore_age>max_restore_test_age_days: issues.append("Restore test is overdue.")
        out.append(BackupFinding(bid,"attention_required" if issues else "metadata_checks_passed",tuple(issues)))
    return out
