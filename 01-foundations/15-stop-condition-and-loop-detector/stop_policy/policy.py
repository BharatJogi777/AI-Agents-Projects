from .detector import StopDecision
def evaluate_stop(*,final_answer:bool,cancelled:bool,deadline_exceeded:bool,step_count:int,max_steps:int,detector_decision:StopDecision|None=None)->StopDecision:
    if step_count<0 or max_steps<1: raise ValueError("step_count must be >= 0 and max_steps >= 1")
    if cancelled: return StopDecision(True,"cancelled")
    if deadline_exceeded: return StopDecision(True,"deadline_exceeded")
    if final_answer: return StopDecision(True,"final_answer")
    if step_count>=max_steps: return StopDecision(True,"step_limit")
    if detector_decision and detector_decision.stop: return detector_decision
    return StopDecision(False,"continue")
