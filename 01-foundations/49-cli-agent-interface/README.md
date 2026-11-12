# AG-049 — CLI agent interface

An argparse boundary around an injected agent function. It validates prompt size, keeps output/error streams injectable for tests, uses deterministic exit codes, and sanitizes exception details.

```bash
python main.py "Summarize the deployment logs"
```

```python
from cli_agent import run_cli
import sys
exit_code=run_cli(["Explain this incident"],agent,sys.stdout,sys.stderr)
```

Exit codes: 0 success, 1 execution/response failure, 2 invalid or oversized input/argument parsing. The included `echo_agent` is only a runnable demonstration; replace it with a real provider-backed agent. Do not expose raw provider exception text to terminal logs.

Test: `python -m pip install pytest && pytest`.
