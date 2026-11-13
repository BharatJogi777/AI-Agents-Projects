"""Choose a deterministic move using a simple minimax search for small games."""
from math import inf
from typing import Callable, Hashable

def minimax(state: Hashable, *, legal_moves: Callable[[Hashable], list[Hashable]], apply_move: Callable[[Hashable,Hashable],Hashable], evaluate: Callable[[Hashable],float], is_terminal: Callable[[Hashable],bool], maximizing: bool, depth: int) -> tuple[Hashable | None,float]:
    if depth<0:
        raise ValueError("depth must be non-negative")
    def search(node: Hashable, remaining: int, max_turn: bool) -> tuple[Hashable | None,float]:
        if remaining==0 or is_terminal(node):
            return None,float(evaluate(node))
        moves=legal_moves(node)
        if not moves:
            return None,float(evaluate(node))
        best_move=None
        best_score=-inf if max_turn else inf
        for move in moves:
            _,score=search(apply_move(node,move),remaining-1,not max_turn)
            if (max_turn and score>best_score) or (not max_turn and score<best_score):
                best_move,best_score=move,score
        return best_move,best_score
    return search(state,depth,maximizing)
