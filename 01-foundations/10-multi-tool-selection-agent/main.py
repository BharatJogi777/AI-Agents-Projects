import argparse
from app import MultiToolAgent, OllamaClient

def main():
    p=argparse.ArgumentParser()
    p.add_argument("prompt")
    p.add_argument("--model",default="qwen3:4b")
    p.add_argument("--base-url",default="http://localhost:11434")
    a=p.parse_args()
    print(MultiToolAgent(OllamaClient(a.model,a.base_url)).run(a.prompt))

if __name__=="__main__": main()
