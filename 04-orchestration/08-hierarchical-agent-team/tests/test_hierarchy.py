import pytest
from app.hierarchy import AgentNode, HierarchicalTeam

def test_leaf_workers_aggregate_through_manager():
    team = HierarchicalTeam({"research": lambda xs: "finding", "write": lambda xs: "draft"})
    tree = AgentNode("root", children=(AgentNode("a", "research"), AgentNode("b", "write")))
    assert team.run(tree) == {"manager": "root", "results": ["finding", "draft"]}

def test_unknown_worker_and_depth_rejected():
    team = HierarchicalTeam({})
    with pytest.raises(ValueError): team.run(AgentNode("root", "missing"))
    deep = AgentNode("1", children=(AgentNode("2", children=(AgentNode("3", "x"),)),))
    with pytest.raises(ValueError): HierarchicalTeam({"x": str}, max_depth=2).run(deep)

def test_cycle_rejected():
    root = AgentNode("root", children=())
    object.__setattr__(root, "children", (root,))
    with pytest.raises(ValueError): HierarchicalTeam({}).run(root)
