from dataclasses import dataclass
from enum import Enum
class Status(str,Enum):
    PENDING="pending";RUNNING="running";SUCCEEDED="succeeded";FAILED="failed";SKIPPED="skipped"
@dataclass
class StepState:
    id:str
    depends_on:tuple[str,...]=()
    status:Status=Status.PENDING
    error:str|None=None
