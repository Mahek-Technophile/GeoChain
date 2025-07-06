import requests

def get_llm_response(query: str) -> str:
    response = requests.post(
        "http://localhost:11434/api/chat",
        json={
            "model": "llama3",
            "messages": [
                {"role": "user", "content": query}
            ]
        }
    )
    return response.json()["message"]["content"]
