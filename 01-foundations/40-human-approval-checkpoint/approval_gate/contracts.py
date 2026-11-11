from dataclasses import dataclass
@dataclass(frozen=True)
class Approval:
    id:str
    action_hash:str
    status:str
    expires_at:float
    reason:str|None=None
class ApprovalNotFound(KeyError):pass
