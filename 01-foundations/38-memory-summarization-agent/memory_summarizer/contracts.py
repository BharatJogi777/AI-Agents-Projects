from dataclasses import dataclass
@dataclass(frozen=True)
class Summary:
    text:str
    source_chars:int
    summary_chars:int
