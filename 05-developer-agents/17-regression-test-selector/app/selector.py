"""Select tests using a declared source-file to test-file impact map."""
from __future__ import annotations
from dataclasses import asdict, dataclass
import json


@dataclass(frozen=True)
class Selection:
    tests: tuple[str, ...]
    unmapped_files: tuple[str, ...]
    changed_files: tuple[str, ...]


def select_tests(changed_files: list[str], impact_map: dict[str, list[str]]) -> Selection:
    if not isinstance(changed_files, list) or any(not isinstance(x, str) or not x.strip() for x in changed_files):
        raise ValueError("changed_files must be a list of non-empty paths")
    if not isinstance(impact_map, dict):
        raise TypeError("impact_map must be a mapping")
    selected, unmapped = set(), []
    for path in dict.fromkeys(changed_files):
        tests = impact_map.get(path)
        if not tests:
            unmapped.append(path)
            continue
        if not isinstance(tests, list) or any(not isinstance(t, str) or not t.strip() for t in tests):
            raise ValueError(f"invalid test mapping for {path}")
        selected.update(tests)
    return Selection(tuple(sorted(selected)), tuple(unmapped), tuple(dict.fromkeys(changed_files)))


def to_json(selection: Selection) -> str:
    return json.dumps(asdict(selection), indent=2)


if __name__ == "__main__":
    print(to_json(select_tests(["app/service.py"], {"app/service.py": ["tests/test_service.py"]})))
