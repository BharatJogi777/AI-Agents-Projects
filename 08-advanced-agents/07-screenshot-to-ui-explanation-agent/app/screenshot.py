"""Create a structured review record for a user-supplied screenshot description."""
from dataclasses import dataclass
@dataclass(frozen=True)
class ScreenshotObservation:
    image_id:str
    page_context:str
    visible_elements:tuple[str,...]
    uncertainty:tuple[str,...]=()
def explain_ui(o:ScreenshotObservation)->dict:
    if not o.image_id.strip() or not o.page_context.strip(): raise ValueError("image identifier and page context are required")
    if not o.visible_elements or any(not e.strip() for e in o.visible_elements): raise ValueError("at least one non-empty visible element is required")
    return {"image_id":o.image_id,"context":o.page_context,"observed_elements":list(o.visible_elements),
            "uncertainties":list(o.uncertainty),"explanation":"Only the listed visible elements are recorded; hidden behavior and intent are unknown.",
            "recommendations_require_human_review":True}
