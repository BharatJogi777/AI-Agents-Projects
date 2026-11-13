from dataclasses import dataclass
@dataclass(frozen=True)
class RollbackRecommendation:
 decision:str
 score:int
 reasons:tuple[str,...]
 requires_human_approval:bool=True
def recommend_rollback(*,error_rate_percent:float,baseline_error_rate_percent:float,latency_p95_ms:float,baseline_latency_p95_ms:float,failed_health_checks:int,customer_impact:bool,rollback_available:bool)->RollbackRecommendation:
 nums=(error_rate_percent,baseline_error_rate_percent,latency_p95_ms,baseline_latency_p95_ms)
 if any(isinstance(x,bool) or not isinstance(x,(int,float)) or x<0 for x in nums): raise ValueError('rates and latency must be non-negative')
 if isinstance(failed_health_checks,bool) or not isinstance(failed_health_checks,int) or failed_health_checks<0: raise ValueError('failed_health_checks must be non-negative integer')
 if not isinstance(customer_impact,bool) or not isinstance(rollback_available,bool): raise ValueError('flags must be boolean')
 score=0; reasons=[]
 if error_rate_percent>max(baseline_error_rate_percent*2,baseline_error_rate_percent+1): score+=35; reasons.append('Error rate materially exceeds baseline')
 if latency_p95_ms>max(baseline_latency_p95_ms*1.5,baseline_latency_p95_ms+100): score+=25; reasons.append('p95 latency materially exceeds baseline')
 if failed_health_checks>=2: score+=25; reasons.append('Multiple health checks are failing')
 if customer_impact: score+=25; reasons.append('Customer impact reported')
 if not rollback_available: reasons.append('Rollback unavailable; escalate to incident command')
 decision='rollback_review_urgent' if score>=50 and rollback_available else 'investigate_and_hold' if score>=25 or not rollback_available else 'continue_observation'
 return RollbackRecommendation(decision,min(score,100),tuple(reasons))
