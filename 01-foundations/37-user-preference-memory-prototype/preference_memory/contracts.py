from dataclasses import dataclass
@dataclass(frozen=True)
class Preference:
    category:str
    value:str
    confirmed_by_user:bool
    recorded_at:str
    provenance:str="explicit_user_confirmation"
