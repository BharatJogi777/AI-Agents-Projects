import argparse
import json
import os

from app.agent import EvidenceBackedEntityExtractor
from app.llm import OllamaClient


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extract entities with exact source evidence using Ollama"
    )
    parser.add_argument("text", help="Source text to analyze")
    parser.add_argument("--model", default=os.getenv("OLLAMA_MODEL", "qwen3:4b"))
    parser.add_argument(
        "--base-url",
        default=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
    )
    parser.add_argument("--timeout", type=float, default=60)
    args = parser.parse_args()

    extractor = EvidenceBackedEntityExtractor(
        OllamaClient(args.base_url, args.model, args.timeout)
    )
    result = extractor.extract(args.text)
    print(json.dumps(result.model_dump(mode="json"), indent=2))


if __name__ == "__main__":
    main()
