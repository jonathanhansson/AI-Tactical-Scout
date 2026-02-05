from pydantic_ai import Agent
from data_models import RagResponse, PlayerShowcase, PlayerShowcaseList
from constants import VECTOR_DB_PATH
from dotenv import load_dotenv

import lancedb
import os

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


player_retriever = Agent(
    model="google-gla:gemini-2.5-flash-lite",
    retries=2,
    system_prompt=(
        "Call the tool retrieve_random_player.",
        "Return EXACTLY the tool output as PlayerShowcaseList.",
        "Do not invent or change any fields."
    ),
    output_type=PlayerShowcaseList
)


@player_retriever.tool_plain
def retrieve_five_players(query: str) -> dict:
    # 1) Fetch a candidate pool (e.g., 30) using vector similarity search
    rows = vector_db["players"].search(query=query).limit(30).to_list()

    # If no results, return an empty list (frontend-safe)
    if not rows:
        return {"players": []}

    # 2) Compute match_percent from LanceDB ranking signal
    # LanceDB usually returns either:
    # - _distance (lower is better)
    # - _score (higher is better)
    if "_distance" in rows[0]:
        vals = [r["_distance"] for r in rows]
        vmin, vmax = min(vals), max(vals)
        
        # Avoid division by zero if all distances are identical
        if vmax == vmin:
            percents = [100.0] * len(rows)
        else:
            # Min distance => 100%
            percents = [round(100 * (vmax - v) / (vmax - vmin), 1) for v in vals]  # min => 100

    elif "_score" in rows[0]:
        vals = [r["_score"] for r in rows]
        vmin, vmax = min(vals), max(vals)
        
        # Avoid division by zero if all scores are identical
        if vmax == vmin:
            percents = [100.0] * len(rows)
        else:
            # Max score => 100%
            percents = [round(100 * (v - vmin) / (vmax - vmin), 1) for v in vals]  # max => 100

    else:
        # Fallback: assign decreasing percentages by rank
        percents = [round(100 - i * 2, 1) for i in range(len(rows))]

    # 3) Take top 5 (results are already sorted best->worst by search)
    top_rows = rows[:5]
    top_percents = percents[:5]

    # 4) Build the exact response shape expected by PlayerShowcaseList
    players = []
    for row, mp in zip(top_rows, top_percents):
        players.append({
            "player_name": row.get("player_name", ""),
            "age": row.get("age", 0),
            "nationality": row.get("nationality", ""),
            "position": row.get("position", ""),
            "current_club": row.get("current_club", ""),
            "asking_price": row.get("asking_price", ""),
            "match_percent": mp,
        })

    return {"players": players}