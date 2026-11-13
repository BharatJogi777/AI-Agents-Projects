import pytest
from app.strategy import minimax

def test_minimax_selects_highest_scoring_move():
    moves={"root":["a","b"]}
    result=minimax("root",legal_moves=lambda s:moves.get(s,[]),apply_move=lambda s,m:m,evaluate=lambda s:{"a":1,"b":5}.get(s,0),is_terminal=lambda s:s in {"a","b"},maximizing=True,depth=2)
    assert result==("b",5.0)

def test_rejects_negative_depth():
    with pytest.raises(ValueError):
        minimax("x",legal_moves=lambda s:[],apply_move=lambda s,m:s,evaluate=lambda s:0,is_terminal=lambda s:True,maximizing=True,depth=-1)
