from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class NormalizationPolicy:
    """Hard limits for converting a tool result into model-facing JSON."""

    max_depth: int = 6
    max_string_chars: int = 4_000
    max_items_per_container: int = 100
    max_output_bytes: int = 16_000
    max_warnings: int = 32

    def __post_init__(self) -> None:
        ranges = {
            "max_depth": (1, 20),
            "max_string_chars": (32, 100_000),
            "max_items_per_container": (1, 10_000),
            "max_output_bytes": (256, 1_000_000),
            "max_warnings": (1, 128),
        }
        for name, (minimum, maximum) in ranges.items():
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, int):
                raise ValueError(f"{name} must be an integer")
            if not minimum <= value <= maximum:
                raise ValueError(f"{name} must be {minimum}..{maximum}")
