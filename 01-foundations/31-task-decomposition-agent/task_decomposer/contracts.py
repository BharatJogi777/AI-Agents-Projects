from dataclasses import dataclass
@dataclass(frozen=True)
class Task:
    id:str
    description:str
    depends_on:tuple[str,...]=()
