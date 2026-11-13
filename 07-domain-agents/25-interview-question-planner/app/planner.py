from dataclasses import dataclass
@dataclass(frozen=True)
class Competency:
    name: str
    level: str
    focus: str
def build_plan(role: str, competencies: list[Competency], questions_per_competency: int = 2) -> dict:
    if not role.strip(): raise ValueError("role is required")
    if not 1<=questions_per_competency<=5: raise ValueError("questions_per_competency must be between 1 and 5")
    if not competencies or any(not c.name.strip() or not c.focus.strip() for c in competencies): raise ValueError("each competency needs a name and focus")
    questions=[]
    for c in competencies:
        for i in range(questions_per_competency):
            questions.append({"competency":c.name,"level":c.level,"question":f"Describe a specific {c.focus} example related to {c.name}. What was your role, what trade-offs did you consider, and what was the outcome?","prompt_number":i+1,"rubric":["specific context","individual contribution","reasoning and trade-offs","measurable outcome"]})
    return {"role":role.strip(),"questions":questions,"evaluation_guidance":"Use the same core rubric for every candidate; assess job-related evidence only.","automated_score":None}
