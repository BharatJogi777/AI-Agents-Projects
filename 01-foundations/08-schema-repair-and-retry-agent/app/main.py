import argparse
import json
import os
import sys

from app.agent import SchemaRepairAgent, SchemaRepairExhausted
from app.llm import OllamaClient


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate schema-valid JSON with bounded repair"
    )
    parser.add_argument("request", help="Work request to convert into structured JSON")
    parser.add_argument("--model", default=os.getenv("OLLAMA_MODEL", "qwen3:4b"))
    parser.add_argument(
        "--base-url", default=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    )
    parser.add_argument("--max-retries", type=int, default=2)
    args = parser.parse_args()

    client = OllamaClient(args.base_url, args.model)
    try:
        agent = SchemaRepairAgent(client, max_retries=args.max_retries)
        result = agent.generate(args.request)
    except SchemaRepairExhausted as exc:
        parser.exit(2, f"Error: {exc} Attempts: {exc.attempts}.\n")
    finally:
        client.close()

    print(json.dumps(result.report.model_dump(mode="json"), indent=2))
    print(
        f"# attempts={result.attempts}, repairs={result.repairs}",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
