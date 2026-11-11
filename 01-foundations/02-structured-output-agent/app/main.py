import argparse
import json
import logging

from app.agent import StructuredOutputAgent
from app.config import Settings
from app.llm import OllamaClient


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze a work request into validated JSON")
    parser.add_argument("text", help="Work request to analyze")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
    settings = Settings()
    agent = StructuredOutputAgent(
        OllamaClient(settings.base_url, settings.model, settings.timeout_seconds)
    )
    result = agent.analyze(args.text)
    print(json.dumps(result.model_dump(mode="json"), indent=2))


if __name__ == "__main__":
    main()
