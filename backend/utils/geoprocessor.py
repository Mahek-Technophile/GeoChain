# backend/utils/geoprocessor.py

def simulate_geoprocessing(steps):
    log = ""
    for i, step in enumerate(steps):
        log += f"Step {i+1}: {step['step']} using {step['tool']}.\n"
        log += f"Reasoning: {step['reasoning']}\n\n"

    return {
        "map_url": "/static/maps/fake_flood_map.png",  # Replace later
        "steps": steps,
        "log": log
    }
