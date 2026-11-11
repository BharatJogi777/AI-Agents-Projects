import argparse
import logging

from app.agent import ToolCallingAgent
from app.config import Settings
from app.llm import OllamaChatClient


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the local Ollama tool-calling agent")
    parser.add_argument("prompt", help="What you want the agent to do")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
    settings = Settings()
    client = OllamaChatClient(
        base_url=settings.base_url,
        model=settings.model,
        timeout_seconds=settings.timeout_seconds,
    )
    agent = ToolCallingAgent(client=client, max_steps=settings.max_steps)
    print(agent.run(args.prompt))


if __name__ == "__main__":
    main()
