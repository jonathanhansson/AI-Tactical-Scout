from pydantic_ai import Agent
from data_models import RagResponse, PlayerShowcase, PlayerShowcaseList
from constants import VECTOR_DB_PATH
from constants import VECTOR_DB_PATH 
from dotenv import load_dotenv

import lancedb

load_dotenv()


vector_db = lancedb.connect(uri=VECTOR_DB_PATH)


rag_agent = Agent(
    model="google-gla:gemini-2.5-flash-lite",
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


# random_player_retriever = Agent(
#     model="google-gla:gemini-2.5-flash",
#     retries=2,
#     system_prompt=(
#         "You are supposed to pick a random player from our vector database.",
#         "Your choice is supposed to be completely random and not biased in any way towards a certain nationality.",
#         "Use the tool retrieve_random_player to get candidates.",
#         "When you output the player, copy match_percent from the chosen candidate (do not invent it)."
#     ),
#     output_type=PlayerShowcase
# )

# @random_player_retriever.tool_plain
# def retrieve_random_player(query: str) -> dict:
#     result = vector_db["players"].search(query=query).to_list()

#     return result


random_player_retriever = Agent(
    model="google-gla:gemini-2.5-flash",
    retries=2,
    system_prompt=(
        "You are supposed to pick 5 random players from our vector database.",
        "Your choice is supposed to be completely random and not biased in any way towards a certain nationality.",
        "Use the tool retrieve_random_player to get candidates.",
        "Return exactly 5 players in the 'players' field.",
        "When you output each player, copy match_percent from the chosen candidate (do not invent it)."
    ),
    output_type=PlayerShowcaseList
)

@random_player_retriever.tool_plain
def retrieve_random_player(query: str) -> dict:
    # Ta en kandidatpool (t.ex. 30) så modellen kan välja 5 slumpmässigt
    candidates = vector_db["players"].search(query=query).limit(4).to_list()
    return {"candidates": candidates}
