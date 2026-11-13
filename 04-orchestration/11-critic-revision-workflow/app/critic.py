from dataclasses import dataclass
from typing import Callable

@dataclass(frozen=True)
class Review:
    feedback: str
    accepted: bool

@dataclass(frozen=True)
class RevisionResult:
    artifact: str
    reviews: tuple[Review, ...]
    accepted: bool

class CriticRevision:
    def __init__(self, critic: Callable[[str], Review], revise: Callable[[str, Review], str], max_rounds: int = 3):
        if max_rounds < 0: raise ValueError("max_rounds cannot be negative")
        self.critic, self.revise, self.max_rounds = critic, revise, max_rounds

    def run(self, artifact: str) -> RevisionResult:
        if not artifact.strip(): raise ValueError("artifact is required")
        history = []
        for _ in range(self.max_rounds + 1):
            review = self.critic(artifact)
            if not isinstance(review, Review) or not isinstance(review.feedback, str):
                raise TypeError("critic must return Review")
            history.append(review)
            if review.accepted: return RevisionResult(artifact, tuple(history), True)
            if len(history) > self.max_rounds: break
            artifact = self.revise(artifact, review)
            if not isinstance(artifact, str) or not artifact.strip():
                raise ValueError("revision must return non-empty text")
        return RevisionResult(artifact, tuple(history), False)
