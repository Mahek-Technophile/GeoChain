from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from utils.llm_client import get_llm_response
from utils.parser import parse_llm_output
from utils.geoprocessor import simulate_geoprocessing

app = FastAPI()

# Enable CORS for local frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    query: str

@app.post("/query")
async def handle_query(input: Query):
    try:
        raw_output = get_llm_response(input.query)
        workflow = parse_llm_output(raw_output)
        result = simulate_geoprocessing(workflow)

        return {
            "map_url": result["map_url"],
            "workflow_steps": result["steps"],
            "log": result["log"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
