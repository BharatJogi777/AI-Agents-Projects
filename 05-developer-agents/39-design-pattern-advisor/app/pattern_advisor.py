"""Suggest candidate patterns from explicit problem signals."""
PATTERNS={
 "varying_algorithms":("Strategy","Encapsulate interchangeable algorithms"),
 "object_creation_complexity":("Factory","Centralize concrete object creation"),
 "event_fanout":("Observer","Publish events to independent subscribers"),
 "cross_cutting_concern":("Decorator","Compose behavior around an object"),
 "complex_subsystem":("Facade","Expose a simpler boundary over collaborators"),
 "workflow_state_transitions":("State","Represent behavior using explicit lifecycle state"),
}
def advise(signals:list[str])->list[dict]:
    if not isinstance(signals,list) or any(not isinstance(s,str) for s in signals): raise ValueError("signals must be a list of strings")
    result=[]
    for signal in dict.fromkeys(signals):
        if signal not in PATTERNS: result.append({"signal":signal,"pattern":None,"reason":"No direct mapping; clarify constraints"})
        else:
            name,reason=PATTERNS[signal]; result.append({"signal":signal,"pattern":name,"reason":reason})
    return result
