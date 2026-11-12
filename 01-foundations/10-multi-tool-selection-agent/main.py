"""Command-line entry point for the multi-tool selection agent."""

import argparse
import logging
import sys

from multi_tool_agent import MultiToolAgent, OllamaClient


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run a bounded multi-tool Ollama agent.")
    parser.add_argument("prompt", help="The task for the agent")
    parser.add_argument("--model", default="qwen3:4b")
    parser.add_argument("--base-url", default="http://localhost:11434")
    parser.add_argument("--max-steps", type=int, default=4)
    parser.add_argument("--verbose", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    logging.basicConfig(
        level=logging.INFO if args.verbose else logging.WARNING,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
    client = OllamaClient(model=args.model, base_url=args.base_url)
    try:
        answer = MultiToolAgent(client, max_steps=args.max_steps).run(args.prompt)
        print(answer)
        return 0
    except (RuntimeError, ValueError) as exc:
        print(f"Agent failed: {exc}", file=sys.stderr)
        return 1
    finally:
        client.close()


if __name__ == "__main__":
    raise SystemExit(main())
