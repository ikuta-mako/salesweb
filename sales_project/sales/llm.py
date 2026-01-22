import requests

# OllamaのAPI設定
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.1"

def call_llm(prompt: str) -> str:
    """
    Ollama（ローカルLLM）にプロンプトを投げて、
    生成結果のテキストだけ返す
    """
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        },
        timeout=60
    )

    response.raise_for_status()

    data = response.json()
    return data.get("response", "")