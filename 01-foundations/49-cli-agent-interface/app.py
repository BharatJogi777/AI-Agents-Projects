"""AG-049: CLI agent interface. Expose an injected agent through argparse with bounded prompt input, deterministic exit codes, and sanitized errors."""
import argparse
from collections.abc import Callable,Sequence
Agent=Callable[[str],str]
def build_parser():
 p=argparse.ArgumentParser(description="Run a text agent"); p.add_argument("prompt"); p.add_argument("--max-chars",type=int,default=4000); return p
def run_cli(argv:Sequence[str]|None,agent:Agent)->int:
 a=build_parser().parse_args(argv)
 if a.max_chars<1 or len(a.prompt)>a.max_chars: print("error: invalid or oversized prompt"); return 2
 try: result=agent(a.prompt)
 except Exception as exc: print(f"agent error: {type(exc).__name__}"); return 1
 if not isinstance(result,str): print("agent error: non-text result"); return 1
 print(result); return 0
def echo_agent(prompt): return f"Received task: {prompt}"
if __name__=="__main__": raise SystemExit(run_cli(None,echo_agent))
