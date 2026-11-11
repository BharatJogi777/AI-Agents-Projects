from dataclasses import dataclass

@dataclass(frozen=True)
class NormalizationPolicy:
    max_depth: int = 6
    max_string_chars: int = 4000
    max_items_per_container: int = 100
    max_output_bytes: int = 16000

    def __post_init__(self):
        if not 1 <= self.max_depth <= 20: raise ValueError("max_depth must be 1..20")
        if not 32 <= self.max_string_chars <= 100000: raise ValueError("max_string_chars must be 32..100000")
        if not 1 <= self.max_items_per_container <= 10000: raise ValueError("max_items_per_container must be 1..10000")
        if not 256 <= self.max_output_bytes <= 1000000: raise ValueError("max_output_bytes must be 256..1000000")
