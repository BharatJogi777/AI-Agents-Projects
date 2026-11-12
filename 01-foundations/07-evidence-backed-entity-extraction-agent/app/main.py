import argparse
import json
import os
from app.agent import EvidenceBackedEntityExtractor
from app.llm import OllamaClient

def main() -> None:
    parser = argparse.ArgumentParser(description="Extract entities with exact source evidence using Ollama")
    parser.add_argument("text", help="Source text to analyze")
    parser.add_argument("--model", default=os.getenv("OLLAMA_MODEL", "qwen3:4b"))
    parser.add_argument("--base-url", default=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"))
    parser.add_argument("--timeout", type=float, default=60)
    args = parser.parse_args()
    client = OllamaClient(args.base_url, args.model, args.timeout)
    try:
        verified = EvidenceBackedEntityExtractor(client).extract_with_evidence(args.text)
        print(json.dumps({
            "source_sha256": verified.source_sha256,
            "entities": verified.result.model_dump(mode="json")["entities"],
            "evidence_matches": [
                {"entity_index": item.entity_index, "value": item.value, "entity_type": item.entity_type,
                 "evidence": item.evidence, "evidence_start": item.evidence_start,
                 "evidence_end": item.evidence_end, "value_start": item.value_start, "value_end": item.value_end}
                for item in verified.evidence_matches
            ],
        }, indent=2))
    finally:
        client.close()

if __name__ == "__main__":
    main()
