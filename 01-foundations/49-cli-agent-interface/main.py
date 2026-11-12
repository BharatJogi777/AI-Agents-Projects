import sys
from cli_agent import echo_agent,run_cli
if __name__=="__main__":
 raise SystemExit(run_cli(None,echo_agent,sys.stdout,sys.stderr))
