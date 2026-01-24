from fastapi import FastAPI
from pydantic import BaseModel, Field
from pydantic_ai.messages import ModelMessage
from backend.rag import rag_agent


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

@app.post("/rag/query")
async def generate_player(request: QueryRequest):
    current_history = chat_histories.get(request.session_id)

    result = await rag_agent.run(request.query, message_history=current_history)

    chat_histories[request.session_id] = result.all_messages()

    return result.output