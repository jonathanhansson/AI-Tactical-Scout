from fastapi import FastAPI
from backend.rag import rag_agent

app = FastAPI()

@app.post("/rag/query")
async def generate_player(query: str):
    result = await rag_agent.run(query)

    return result.output