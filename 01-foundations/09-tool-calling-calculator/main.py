import argparse
import os
from app import CalculatorAgent, OllamaChatClient


def main():
    parser = argparse.ArgumentParser(description="Ask an Ollama model to calculate using a deterministic tool.")
    parser.add_argument("request", help="Natural-language arithmetic request")
    parser.add_argument("--model", default=os.getenv("OLLAMA_MODEL", "qwen3:4b"))
    parser.add_argument("--base-url", default=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"))
    args = parser.parse_args()
    print(CalculatorAgent(OllamaChatClient(args.base_url, args.model)).run(args.request))


if __name__ == "__main__":
    main()
