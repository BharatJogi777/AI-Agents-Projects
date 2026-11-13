"""Create a structured disaster-recovery exercise plan."""
from dataclasses import dataclass

@dataclass(frozen=True)
class DrillPlan:
    system: str
    objectives: tuple[str,...]
    exercises: tuple[str,...]
    evidence_to_collect: tuple[str,...]
    safety_gates: tuple[str,...]

def plan_drill(system: str, *, rto_minutes: int, rpo_minutes: int, tier: str, production_exercise: bool=False) -> DrillPlan:
    if not isinstance(system,str) or not system.strip(): raise ValueError("system must be a non-empty string")
    if any(isinstance(v,bool) or not isinstance(v,int) or v<0 for v in (rto_minutes,rpo_minutes)): raise ValueError("RTO and RPO must be non-negative integers")
    if tier not in {"critical","high","standard"}: raise ValueError("tier must be critical, high, or standard")
    exercises=["Review dependency and recovery runbooks","Validate backup inventory and last successful restore evidence","Walk through failover decision points using a tabletop scenario","Record measured recovery and data-loss estimates"]
    if tier in {"critical","high"}: exercises.insert(2,"Conduct a controlled restore rehearsal in an isolated environment")
    if production_exercise: exercises.append("Production failover simulation only after change approval, stakeholder notification, and tested abort criteria")
    evidence=("Timestamped recovery milestones","Observed recovery time compared with RTO","Observed data-loss window compared with RPO","Restore integrity and application smoke-test results","Approvals, deviations, and follow-up owners")
    gates=("Name an incident commander and system owner","Use isolated/non-production systems by default","Confirm backups and rollback/abort procedure before any live exercise","Obtain explicit change approval for production-impacting steps")
    return DrillPlan(system.strip(),(f"RTO <= {rto_minutes} minutes",f"RPO <= {rpo_minutes} minutes"),tuple(exercises),evidence,gates)
