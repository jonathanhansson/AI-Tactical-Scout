from fastapi import FastAPI
from pydantic import BaseModel, Field
from pydantic_ai.messages import ModelMessage
from rag import rag_agent, player_retriever
import lancedb
from constants import VECTOR_DB_PATH

from rag import rag_agent, player_retriever
from constants import VECTOR_DB_PATH

import lancedb


"""
We import pydantic_ai.messages to be able to store
chat histories, so that the model can use the 
history as context. 'chat_histories' is now a dict
where the key is a string and the value a list of 
ModelMessage
"""
chat_histories: dict[str, list[ModelMessage]] = {}


class QueryRequest(BaseModel):
    query: str
    session_id: str = Field(default="default", description="Unique id for the conversation.")


app = FastAPI()
db = lancedb.connect(uri=VECTOR_DB_PATH)

@app.post("/rag/query")
async def generate_player(request: QueryRequest):
    current_history = chat_histories.get(request.session_id)

    result = await rag_agent.run(request.query, message_history=current_history)

    chat_histories[request.session_id] = result.all_messages()

    return result.output


@app.post("/list_five_players")
async def list_five_players_based_on_search(request: QueryRequest):
    result = await player_retriever.run(request.query)

    return result.output


@app.get("/players")
def list_players(limit: int = 50):
    rows = db["players"].to_pandas().head(limit)
    # return minimal
    return {"players": rows["player_name"].tolist()}


@app.get("/health")
def health():
    return {"status": "ok"}