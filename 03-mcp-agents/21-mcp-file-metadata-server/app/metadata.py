"""Inspect metadata for files under a configured root without reading contents."""
from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class FileMetadata:
    name: str
    relative_path: str
    size_bytes: int
    modified_ns: int
    is_directory: bool

class MetadataService:
    def __init__(self,root: str|Path):
        self.root=Path(root).resolve(strict=True)
        if not self.root.is_dir():
            raise ValueError("root must be a directory")

    def inspect(self,relative_path: str)->FileMetadata:
        candidate=(self.root/relative_path).resolve(strict=True)
        if not candidate.is_relative_to(self.root):
            raise PermissionError("path escapes configured root")
        stat=candidate.stat()
        return FileMetadata(candidate.name,candidate.relative_to(self.root).as_posix(),stat.st_size,stat.st_mtime_ns,candidate.is_dir())
