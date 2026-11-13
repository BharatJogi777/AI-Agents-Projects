"""Read-only Git metadata using subprocess without shell interpolation."""
import subprocess
from pathlib import Path

class GitRepositoryReader:
    def __init__(self,root: str|Path,*,timeout: float=3.0):
        self.root=Path(root).resolve(strict=True)
        if not (self.root/".git").exists():
            raise ValueError("root is not a Git repository")
        if timeout<=0:
            raise ValueError("timeout must be positive")
        self.timeout=timeout

    def _run(self,*args: str)->str:
        result=subprocess.run(["git","-C",str(self.root),*args],capture_output=True,text=True,timeout=self.timeout,check=False)
        if result.returncode:
            raise RuntimeError("git inspection failed")
        return result.stdout.strip()

    def current_branch(self)->str:
        return self._run("branch","--show-current")

    def latest_commit(self)->dict[str,str]:
        values=self._run("log","-1","--format=%H%n%an%n%s").splitlines()
        if len(values)!=3:
            raise RuntimeError("unexpected git log output")
        return {"sha":values[0],"author":values[1],"subject":values[2]}

    def status(self)->list[str]:
        output=self._run("status","--short")
        return output.splitlines() if output else []
