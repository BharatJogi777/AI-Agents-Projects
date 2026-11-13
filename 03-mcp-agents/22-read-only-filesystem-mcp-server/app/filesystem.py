"""Read-only workspace service confined to a configured root."""
from pathlib import Path

class ReadOnlyWorkspace:
    def __init__(self,root: str|Path,*,max_bytes: int=1_000_000):
        self.root=Path(root).resolve(strict=True)
        if not self.root.is_dir() or max_bytes<1:
            raise ValueError("root must be a directory and max_bytes positive")
        self.max_bytes=max_bytes

    def _resolve(self,relative_path: str)->Path:
        path=(self.root/relative_path).resolve(strict=True)
        if not path.is_relative_to(self.root):
            raise PermissionError("path escapes workspace")
        if not path.is_file():
            raise IsADirectoryError(relative_path)
        return path

    def list_files(self,relative_dir: str=".")->list[str]:
        directory=(self.root/relative_dir).resolve(strict=True)
        if not directory.is_relative_to(self.root):
            raise PermissionError("path escapes workspace")
        if not directory.is_dir():
            raise NotADirectoryError(relative_dir)
        return sorted(item.relative_to(self.root).as_posix() for item in directory.iterdir() if item.is_file() and item.resolve().is_relative_to(self.root))

    def read_text(self,relative_path: str)->str:
        path=self._resolve(relative_path)
        if path.stat().st_size>self.max_bytes:
            raise ValueError("file exceeds configured read limit")
        return path.read_text(encoding="utf-8")
