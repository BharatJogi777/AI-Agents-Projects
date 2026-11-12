import argparse
import os
import sys

from calculator_core.agent import CalculatorAgent, AgentStepLimitError
from calculator_core.provider import OllamaChatClient


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Ask an Ollama model to calculate using a deterministic tool."
    )
    parser.add_argument("request", help="Natural-language arithmetic request")
    parser.add_argument("--model", default=os.getenv("OLLAMA_MODEL", "qwen3:4b"))
    parser.add_argument(
        "--base-url", default=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    )
    parser.add_argument("--max-steps", type=int, default=3)
    args = parser.parse_args()

    client = OllamaChatClient(args.base_url, args.model)
    try:
        result = CalculatorAgent(client, max_steps=args.max_steps).run(args.request)
    except (AgentStepLimitError, RuntimeError, ValueError) as exc:
        parser.exit(2, f"Error: {exc}\n")
    finally:
        client.close()

    print(result)


if __name__ == "__main__":
    main()
