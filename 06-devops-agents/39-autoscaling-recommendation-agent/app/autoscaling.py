"""Generate reviewable autoscaling recommendations from supplied metrics."""
from dataclasses import dataclass

@dataclass(frozen=True)
class ScalingRecommendation:
    action: str
    proposed_min: int
    proposed_max: int
    target_utilization: float
    rationale: str
    requires_approval: bool=True

def recommend_scaling(*, current_min: int, current_max: int, desired: int, cpu_percent: float, queue_depth: int, max_step: int=2) -> ScalingRecommendation:
    vals=(current_min,current_max,desired,queue_depth,max_step)
    if any(isinstance(v,bool) or not isinstance(v,int) for v in vals): raise ValueError("capacity and queue values must be integers")
    if current_min<0 or current_max<1 or current_min>current_max or not current_min<=desired<=current_max or queue_depth<0 or max_step<1: raise ValueError("invalid scaling bounds or metrics")
    if isinstance(cpu_percent,bool) or not isinstance(cpu_percent,(int,float)) or not 0<=cpu_percent<=100: raise ValueError("cpu_percent must be in [0,100]")
    if cpu_percent>=80 or queue_depth>=1000:
        new_max=min(current_max+max_step,max(current_max,desired+max_step)); new_min=min(current_min+1,new_max)
        return ScalingRecommendation("scale_out",new_min,new_max,60.0,"High CPU or queue depth suggests pressure; increase capacity gradually and inspect downstream limits.")
    if cpu_percent<=25 and queue_depth==0 and current_max>current_min:
        new_max=max(current_min,current_max-1); new_min=min(current_min,new_max)
        return ScalingRecommendation("consider_scale_in",new_min,new_max,65.0,"Low utilization and empty queue suggest possible excess capacity; verify peak patterns before reducing.")
    return ScalingRecommendation("no_change",current_min,current_max,70.0,"Signals do not cross configured scaling thresholds.")
