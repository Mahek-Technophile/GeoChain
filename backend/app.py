# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import geopandas as gpd
import traceback

OLLAMA_API_URL = "http://localhost:11434/api/generate"  # Ollama default API endpoint
OLLAMA_MODEL = "llama3"  # Change if you use a different model

app = Flask(__name__)
CORS(app)

def query_ollama(prompt):
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(OLLAMA_API_URL, json=payload)
    response.raise_for_status()
    return response.json()["response"]

def parse_llm_output(llm_output):
    """
    Assumes LLM returns a JSON block with 'workflow' and 'reasoning'.
    Adjust this function if your prompt/LLM output format is different.
    """
    import json
    try:
        # Try to extract JSON from the LLM output
        start = llm_output.find('{')
        end = llm_output.rfind('}') + 1
        workflow_json = llm_output[start:end]
        data = json.loads(workflow_json)
        return data.get("workflow", []), data.get("reasoning", [])
    except Exception:
        # Fallback: return the raw output for debugging
        return [], llm_output

@app.route("/api/query", methods=["POST"])
def handle_query():
    try:
        data = request.json
        user_query = data.get("query", "")
        if not user_query:
            return jsonify({"error": "No query provided"}), 400

        # Prompt template for LLM
        prompt = (
            "You are a GIS expert. Given the user query below, "
            "generate a step-by-step geospatial workflow in JSON format, "
            "with a 'workflow' array (steps as objects with 'tool', 'operation', 'parameters'), "
            "and a 'reasoning' array (explain each step):\n"
            f"User Query: {user_query}\n"
            "Respond ONLY with a JSON object."
        )

        llm_output = query_ollama(prompt)
        workflow, reasoning = parse_llm_output(llm_output)

        # For demonstration, execute only the first step if it's a GeoPandas operation
        results = []
        logs = []
        for step in workflow:
            tool = step.get("tool", "").lower()
            operation = step.get("operation", "").lower()
            params = step.get("parameters", {})
            try:
                if tool == "geopandas" and operation == "read_file":
                    # Example: read a shapefile/geojson
                    gdf = gpd.read_file(params["filepath"])
                    results.append(gdf.head().to_json())
                    logs.append(f"Loaded file {params['filepath']}")
                # Add more tool/operation handling as needed
            except Exception as e:
                logs.append(f"Error in step: {step} - {str(e)}")
                continue

        return jsonify({
            "workflow": workflow,
            "reasoning": reasoning,
            "results": results,
            "logs": logs,
            "llm_raw": llm_output
        })
    except Exception as e:
        return jsonify({"error": str(e), "trace": traceback.format_exc()}), 500

if __name__ == "__main__":
    app.run(port=5000, debug=True)
