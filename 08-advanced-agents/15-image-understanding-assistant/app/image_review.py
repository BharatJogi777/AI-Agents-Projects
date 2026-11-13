from dataclasses import dataclass
@dataclass(frozen=True)
class ImageObservation:
    image_ref:str
    observed_objects:tuple[str,...]
    visible_text:tuple[str,...]=()
    uncertain_details:tuple[str,...]=()
def describe_observation(o:ImageObservation)->dict:
    if not o.image_ref.strip(): raise ValueError("image reference is required")
    if any(not x.strip() for x in (*o.observed_objects,*o.visible_text,*o.uncertain_details)): raise ValueError("observation entries cannot be blank")
    return {"image_ref":o.image_ref,"observed_objects":list(o.observed_objects),"visible_text":list(o.visible_text),
            "uncertain_details":list(o.uncertain_details),"claims_limited_to_observations":True,"identity_or_context_inferred":False}
