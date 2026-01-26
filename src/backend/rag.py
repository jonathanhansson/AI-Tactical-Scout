from pydantic_ai import Agent
from backend.data_models import RagResponse, PlayerShowcase
from backend.constants import VECTOR_DB_PATH
from dotenv import load_dotenv

import lancedb

load_dotenv()


vector_db = lancedb.connect(uri=VECTOR_DB_PATH)


rag_agent = Agent(
    model="google-gla:gemini-2.5-flash",
    retries=2,
    system_prompt=(
        "You are an expert in football (soccer) scouting.",
        "Always answer based on retrieved knowledge (.txt files), but you CAN mix in your expertise (training data) to make the answer more coherent.",
        "Don't hallucinate, rather say you can't answer it if the user prompt is outside your knowledge.",
        "Keep answers clear and concise. Max 6 sentences."
    ),
    output_type=RagResponse
)


@rag_agent.tool_plain
def retrieve_first_and_second_pick(query: str, k=2):
    # This uses vector search

    results = vector_db["players"].search(query=query).limit(k).to_list()
    top_result = results[0]


    return f"""
    Player name: {top_result["player_name"]},
    Filepath: {top_result["filepath"]},
    Answer: {top_result["scouting_report"]}
    """


random_player_retriever = Agent(
    model="google-gla:gemini-2.5-flash",
    retries=2,
    system_prompt=(
        "You are supposed to pick a random player from our vector database.",
        "Your choice is supposed to be completely random and not biased in any way towards a certain nationality."
    ),
    output_type=PlayerShowcase
)


@random_player_retriever.tool_plain
def retrieve_random_player(query: str) -> dict:
    result = vector_db["players"].search(query=query).to_list()

    return result



def search_players(query: str, k: int = 5):
    results = vector_db["players"].search(query=query).limit(k).to_list()
    # returnera “lätta” objekt till frontend
    return [
        {
            "player_name": r["player_name"],
            "filepath": r["filepath"],
            "nationality": r.get("nationality"),
            "position": r.get("position"),
            "age": r.get("age"),
            "preview": (r["scouting_report"][:300] + "...") if r.get("scouting_report") else None,
        }
        for r in results
    ]