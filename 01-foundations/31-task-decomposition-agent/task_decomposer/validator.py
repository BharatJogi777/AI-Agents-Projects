from .contracts import Task
class TaskGraphError(ValueError): pass
def validate_tasks(tasks,max_tasks=30):
    if type(max_tasks) is not int or max_tasks<1: raise ValueError("max_tasks must be positive")
    if not isinstance(tasks,(list,tuple)) or not 1<=len(tasks)<=max_tasks: raise TaskGraphError("task count out of bounds")
    by={}
    for task in tasks:
        if not isinstance(task,Task): raise TaskGraphError("every item must be a Task")
        if not isinstance(task.id,str) or not task.id.strip() or len(task.id)>80 or task.id in by: raise TaskGraphError("invalid or duplicate task ID")
        if not isinstance(task.description,str) or not task.description.strip() or len(task.description)>500: raise TaskGraphError(f"invalid description: {task.id}")
        if not isinstance(task.depends_on,tuple) or any(not isinstance(x,str) or not x for x in task.depends_on): raise TaskGraphError(f"invalid dependencies: {task.id}")
        if len(set(task.depends_on))!=len(task.depends_on): raise TaskGraphError(f"duplicate dependencies: {task.id}")
        by[task.id]=task
    for task in tasks:
        if task.id in task.depends_on or any(dep not in by for dep in task.depends_on): raise TaskGraphError(f"unknown or self dependency: {task.id}")
    visiting=set();visited=set();ordered=[]
    def visit(key):
        if key in visiting: raise TaskGraphError("dependency cycle detected")
        if key in visited:return
        visiting.add(key)
        for dep in by[key].depends_on:visit(dep)
        visiting.remove(key);visited.add(key);ordered.append(by[key])
    for key in by:visit(key)
    return tuple(ordered)
