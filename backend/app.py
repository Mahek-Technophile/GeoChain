from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from utils.llm_client import get_llm_response

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
        print("LLM Raw Output:\n", raw_output)
        return {"llm_output": raw_output}
    except Exception as e:
        print("ERROR:", str(e))
        return {"error": str(e)}
