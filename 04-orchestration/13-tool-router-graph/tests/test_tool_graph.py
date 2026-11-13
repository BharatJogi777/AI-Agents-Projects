import pytest
from app.tool_graph import ToolRequest, ToolResult, ToolRouterGraph

def test_routes_between_allowlisted_tools():
    graph = ToolRouterGraph({
        "lookup": lambda args: ToolResult("lookup", "data", "summarize"),
        "summarize": lambda args: ToolResult("summarize", args["previous"] + " done"),
    })
    result = graph.run(ToolRequest("lookup", {}))
    assert [x.tool for x in result] == ["lookup", "summarize"]
    assert result[-1].output == "data done"

def test_unknown_next_tool_rejected():
    graph = ToolRouterGraph({"a": lambda a: ToolResult("a", 1, "missing")})
    with pytest.raises(ValueError): graph.run(ToolRequest("a", {}))

def test_hop_limit_enforced():
    graph = ToolRouterGraph({"a": lambda a: ToolResult("a", 1, "a")}, 2)
    with pytest.raises(RuntimeError): graph.run(ToolRequest("a", {}))
