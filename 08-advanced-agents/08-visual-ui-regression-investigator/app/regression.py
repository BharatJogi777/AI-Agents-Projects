"""Compare precomputed visual metrics; image capture and pixel analysis are external."""
from dataclasses import dataclass
@dataclass(frozen=True)
class VisualMetrics:
    build_id:str
    screenshot_hash:str
    element_count:int
    layout_score:float
def investigate(baseline:VisualMetrics,current:VisualMetrics,minimum_layout_score:float=0.98)->dict:
    if not baseline.build_id or not current.build_id or not baseline.screenshot_hash or not current.screenshot_hash: raise ValueError("build IDs and screenshot hashes are required")
    if baseline.element_count<0 or current.element_count<0: raise ValueError("element counts cannot be negative")
    if not 0<=minimum_layout_score<=1 or not 0<=current.layout_score<=1: raise ValueError("layout scores must be between zero and one")
    changed=baseline.screenshot_hash!=current.screenshot_hash or baseline.element_count!=current.element_count
    return {"changed":changed,"layout_below_threshold":current.layout_score<minimum_layout_score,
            "element_count_delta":current.element_count-baseline.element_count,
            "review_required":changed or current.layout_score<minimum_layout_score}
