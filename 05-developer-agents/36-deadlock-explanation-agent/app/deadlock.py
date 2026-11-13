"""Find cycles in a wait-for graph."""
def explain(wait_for: dict[str,list[str]]) -> list[dict]:
    if not isinstance(wait_for,dict): raise ValueError("wait_for must be a mapping")
    graph={}
    for owner, blockers in wait_for.items():
        if not isinstance(owner,str) or not owner.strip() or not isinstance(blockers,list): raise ValueError("Owners must be names and blockers must be lists")
        if any(not isinstance(x,str) or not x.strip() for x in blockers): raise ValueError("Blocker names must be non-empty")
        graph[owner]=blockers[:]
    nodes=set(graph)
    for deps in graph.values(): nodes.update(deps)
    state={}; stack=[]; cycles=set()
    def visit(node):
        state[node]=1; stack.append(node)
        for nxt in graph.get(node,[]):
            if state.get(nxt,0)==0: visit(nxt)
            elif state.get(nxt)==1:
                cycle=stack[stack.index(nxt):]
                rotations=[tuple(cycle[i:]+cycle[:i]) for i in range(len(cycle))]
                cycles.add(min(rotations))
        stack.pop(); state[node]=2
    for node in sorted(nodes):
        if state.get(node,0)==0: visit(node)
    return [{"cycle":list(c)+[c[0]],"explanation":"Each participant waits for the next, forming circular wait."} for c in sorted(cycles)]
