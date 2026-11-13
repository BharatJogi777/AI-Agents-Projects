from app.graph_exporter import Node, Edge, WorkflowGraph
import pytest

def test_dot_export_and_escaping():
    graph = WorkflowGraph([Node("start", 'Start "here"'), Node("done")], [Edge("start", "done", "ok")])
    dot = graph.to_dot()
    assert 'Start \\"here\\"' in dot and '"start" -> "done"' in dot

def test_unknown_edge_rejected():
    with pytest.raises(ValueError): WorkflowGraph([Node("a")], [Edge("a", "missing")]).to_dot()

def test_duplicate_ids_rejected():
    with pytest.raises(ValueError): WorkflowGraph([Node("a"), Node("a")]).to_dot()
