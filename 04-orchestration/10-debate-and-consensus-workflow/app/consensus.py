from collections import Counter
from dataclasses import dataclass
from typing import Callable

@dataclass(frozen=True)
class Position:
    agent: str
    choice: str
    rationale: str = ""

@dataclass(frozen=True)
class Consensus:
    choice: str | None
    votes: dict[str, int]
    reached: bool

class ConsensusWorkflow:
    def __init__(self, agents: dict[str, Callable[[str], Position]], quorum: int | None = None):
        if not agents:
            raise ValueError("at least one agent is required")
        if quorum is not None and not 1 <= quorum <= len(agents):
            raise ValueError("invalid quorum")
        self.agents, self.quorum = dict(agents), quorum or len(agents)

    def run(self, question: str) -> Consensus:
        if not question or not question.strip():
            raise ValueError("question is required")
        votes = Counter()
        for name, agent in self.agents.items():
            position = agent(question)
            if not isinstance(position, Position) or position.agent != name or not position.choice.strip():
                raise ValueError(f"agent {name} returned invalid position")
            votes[position.choice] += 1
        ranked = votes.most_common()
        winner, count = ranked[0]
        tied = len(ranked) > 1 and ranked[1][1] == count
        reached = not tied and count >= self.quorum
        return Consensus(winner if reached else None, dict(votes), reached)
