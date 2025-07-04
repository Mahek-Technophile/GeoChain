# backend/utils/parser.py

import json

def parse_llm_output(output_str):
    try:
        parsed = json.loads(output_str)
        return parsed.get("steps", [])
    except Exception as e:
        return []
