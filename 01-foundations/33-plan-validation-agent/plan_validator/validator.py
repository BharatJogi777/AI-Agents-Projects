from .contracts import Step,Validation
def validate_plan(steps,max_steps=20,allowed_risks=("low","medium"))->Validation:
    errors=[];order=[]
    if type(max_steps) is not int or max_steps<1:return Validation(False,("invalid_max_steps",))
    if not isinstance(steps,(list,tuple)) or not steps or len(steps)>max_steps:return Validation(False,("step_count_out_of_bounds",))
    if not isinstance(allowed_risks,(tuple,list,set,frozenset)) or any(not isinstance(x,str) for x in allowed_risks):return Validation(False,("invalid_risk_policy",))
    if any(not isinstance(s,Step) for s in steps):return Validation(False,("invalid_step_type",))
    ids=[s.id for s in steps]
    if any(not isinstance(x,str) or not x.strip() for x in ids) or len(set(ids))!=len(ids):errors.append("duplicate_or_empty_ids")
    known={x for x in ids if isinstance(x,str)};graph={}
    for s in steps:
        if not isinstance(s.action,str) or not s.action.strip() or len(s.action)>500:errors.append(f"invalid_action:{s.id}")
        if not isinstance(s.risk,str) or s.risk not in allowed_risks:errors.append(f"risk_not_allowed:{s.id}")
        if not isinstance(s.depends_on,tuple) or any(not isinstance(d,str) for d in s.depends_on) or len(set(s.depends_on))!=len(s.depends_on) or any(d not in known or d==s.id for d in s.depends_on):errors.append(f"invalid_dependencies:{s.id}")
        graph[s.id]=s.depends_on if isinstance(s.depends_on,tuple) and all(isinstance(d,str) for d in s.depends_on) else ()
    visiting=set();visited=set()
    def visit(node):
        if node in visiting:raise ValueError()
        if node in visited:return
        visiting.add(node)
        for dep in graph.get(node,()):
            if dep in graph:visit(dep)
        visiting.remove(node);visited.add(node);order.append(node)
    try:
        for node in graph:visit(node)
    except ValueError:errors.append("dependency_cycle");order=[]
    unique=tuple(dict.fromkeys(errors))
    return Validation(not unique,unique,tuple(order) if not unique else ())
