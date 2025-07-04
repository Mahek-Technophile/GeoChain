import requests

def get_llm_response(user_query: str) -> str:
    prompt = f"""
You are a geospatial analyst. Break down the following user query into a detailed step-by-step GIS workflow using real geoprocessing tools and open datasets. Then explain your reasoning.

Query: {user_query}

Respond in this format:

[STEPS]
1. ...
2. ...
[REASONING]
...
"""
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
    )
    return response.json()["response"]
