"""Generate bounded, harmless input perturbations for robustness testing."""
from dataclasses import dataclass

@dataclass(frozen=True)
class AdversarialCase:
    case_id: str
    variant: str
    input_text: str

def generate_adversarial_cases(text: str, *, max_cases: int = 5) -> tuple[AdversarialCase,...]:
    if not isinstance(text,str) or not text: raise ValueError("text must be non-empty")
    if not isinstance(max_cases,int) or isinstance(max_cases,bool) or not 0 <= max_cases <= 5: raise ValueError("max_cases must be between 0 and 5")
    variants=[("leading_space"," "+text),("trailing_space",text+" "),("mixed_case",text.swapcase()),
              ("unicode_whitespace",text.replace(" ","\u00a0")),("repeated_input",text+" "+text)]
    return tuple(AdversarialCase(f"adv-{i+1:02d}",name,value) for i,(name,value) in enumerate(variants[:max_cases]))
