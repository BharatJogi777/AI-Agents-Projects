"""Detect repeated agent states and enforce explicit stop conditions."""
import hashlib
import json
from dataclasses import dataclass


@dataclass(frozen=True)
class StopDecision:
    stop: bool
    reason: str


class LoopDetector:
    def __init__(self, max_repeats: int = 2, history_size: int = 20):
        if max_repeats < 1 or history_size < max_repeats: raise ValueError("invalid repeat/history limits")
        self.max_repeats,self.history_size=max_repeats,history_size
        self._recent: list[str]=[]

    @staticmethod
    def fingerprint(state) -> str:
        encoded=json.dumps(state,sort_keys=True,separators=(",",":"),default=str)
        return hashlib.sha256(encoded.encode()).hexdigest()

    def observe(self,state) -> StopDecision:
        key=self.fingerprint(state)
        repeats=self._recent.count(key)
        self._recent.append(key)
        self._recent=self._recent[-self.history_size:]
        if repeats >= self.max_repeats:
            return StopDecision(True,"repeated_state")
        return StopDecision(False,"continue")


def evaluate_stop(*,final_answer:bool, cancelled:bool, deadline_exceeded:bool,
                  step_count:int,max_steps:int,detector_decision:StopDecision|None=None)->StopDecision:
    if cancelled: return StopDecision(True,"cancelled")
    if deadline_exceeded: return StopDecision(True,"deadline_exceeded")
    if final_answer: return StopDecision(True,"final_answer")
    if step_count >= max_steps: return StopDecision(True,"step_limit")
    if detector_decision and detector_decision.stop: return detector_decision
    return StopDecision(False,"continue")
