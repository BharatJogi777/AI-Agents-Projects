import argparse,sys
from collections.abc import Callable,Sequence
from typing import TextIO
Agent=Callable[[str],str]
class CLIError(ValueError):pass
def build_parser():
 p=argparse.ArgumentParser(description="Run an injected text agent")
 p.add_argument("prompt",help="task or question for the agent")
 p.add_argument("--max-chars",type=int,default=4000,help="maximum prompt length")
 return p
def run_cli(argv:Sequence[str]|None,agent:Agent,stdout:TextIO|None=None,stderr:TextIO|None=None)->int:
 if not callable(agent):raise TypeError("agent must be callable")
 stdout=stdout or sys.stdout;stderr=stderr or sys.stderr
 try:args=build_parser().parse_args(argv)
 except SystemExit as exc:return int(exc.code)
 if args.max_chars<1 or len(args.prompt)>args.max_chars:
  print("error: prompt exceeds configured limit",file=stderr);return 2
 try:result=agent(args.prompt)
 except Exception as exc:
  print(f"agent error: {type(exc).__name__}",file=stderr);return 1
 if not isinstance(result,str):
  print("agent error: invalid response type",file=stderr);return 1
 print(result,file=stdout);return 0
def echo_agent(prompt:str)->str:return f"Received task: {prompt}"
