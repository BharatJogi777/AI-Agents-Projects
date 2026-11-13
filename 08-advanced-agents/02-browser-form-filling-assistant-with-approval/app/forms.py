from dataclasses import dataclass
import hashlib,json
@dataclass(frozen=True)
class FormDraft:
    origin:str
    fields:dict[str,str]
def prepare_draft(origin:str,fields:dict[str,str],allowed_origins:set[str])->FormDraft:
    if origin not in allowed_origins: raise ValueError("form origin is not allowlisted")
    if not fields or any(not k.strip() or not isinstance(v,str) for k,v in fields.items()): raise ValueError("form fields must have non-empty names and string values")
    return FormDraft(origin,dict(fields))
def approval_token(draft:FormDraft)->str:
    return hashlib.sha256(json.dumps({"origin":draft.origin,"fields":draft.fields},sort_keys=True).encode()).hexdigest()
def authorize_submission(draft:FormDraft,supplied_token:str)->dict:
    if not supplied_token or supplied_token!=approval_token(draft): raise PermissionError("explicit approval for this exact draft is required")
    return {"authorized":True,"origin":draft.origin,"fields":dict(draft.fields),"submission_performed":False}
