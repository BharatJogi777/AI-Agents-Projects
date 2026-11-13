from dataclasses import dataclass
@dataclass(frozen=True)
class Lesson:
    lesson_id: str
    title: str
    learning_objectives: tuple[str,...]
    source_refs: tuple[str,...]
    estimated_minutes: int
def prepare_lesson(lesson: Lesson, audience_level: str, max_minutes: int=60) -> dict:
    if not lesson.lesson_id.strip() or not lesson.title.strip(): raise ValueError("lesson id and title are required")
    if audience_level not in {"beginner","intermediate","advanced"}: raise ValueError("unsupported audience level")
    if not lesson.learning_objectives or any(not x.strip() for x in lesson.learning_objectives): raise ValueError("non-empty learning objectives are required")
    if not lesson.source_refs or any(not x.strip() for x in lesson.source_refs): raise ValueError("source references are required")
    if lesson.estimated_minutes<=0 or max_minutes<=0: raise ValueError("lesson duration and limit must be positive")
    return {"lesson_id":lesson.lesson_id,"title":lesson.title,"audience_level":audience_level,"objectives":list(lesson.learning_objectives),"sources":list(lesson.source_refs),"estimated_minutes":min(lesson.estimated_minutes,max_minutes),"duration_trimmed":lesson.estimated_minutes>max_minutes,"content_generated":False,"educator_review_required":True}
