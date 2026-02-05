from pydantic_ai import Agent
from data_models import RagResponse, PlayerShowcase, PlayerShowcaseList
from constants import VECTOR_DB_PATH
from constants import VECTOR_DB_PATH 
from dotenv import load_dotenv
import re
import lancedb

load_dotenv()

print("### USING rag.py FROM:", __file__)


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


def extract_from_player_data(label: str, report: str, default=""):
    """
    Extracts 'Label: value' from the PLAYER DATA section.
    """
    m_section = re.search(
        r"PLAYER DATA\s*-*\s*(.*)$",
        report,
        flags=re.IGNORECASE | re.DOTALL
    )
    if not m_section:
        return default

    section = m_section.group(1)

    m_value = re.search(
        rf"{re.escape(label)}\s*:\s*([^\n\r]+)",
        section,
        flags=re.IGNORECASE
    )
    return m_value.group(1).strip() if m_value else default


player_retriever = Agent(
    model="google-gla:gemini-2.5-flash-lite",
    retries=2,
    system_prompt=(
        "Call the tool retrieve_five_players.",
        "Return EXACTLY the tool output as PlayerShowcaseList.",
        "Do not invent or change any fields."
    ),
    output_type=PlayerShowcaseList
)


@player_retriever.tool_plain
def retrieve_five_players(query: str) -> dict:
    rows = vector_db["players"].search(query=query).limit(30).to_list()
    print("TOTAL HITS FROM DB:", len(rows))

    if not rows:
        return {"players": []}

    if "_distance" in rows[0]:
        vals = [r["_distance"] for r in rows]
        vmin, vmax = min(vals), max(vals)
        percents = [100.0] * len(rows) if vmax == vmin else [round(100 * (vmax - v) / (vmax - vmin), 1) for v in vals]
    elif "_score" in rows[0]:
        vals = [r["_score"] for r in rows]
        vmin, vmax = min(vals), max(vals)
        percents = [100.0] * len(rows) if vmax == vmin else [round(100 * (v - vmin) / (vmax - vmin), 1) for v in vals]
    else:
        percents = [round(100 - i * 2, 1) for i in range(len(rows))]

    top_rows = rows[:5]
    top_percents = percents[:5]

    print("TOP_ROWS:", len(top_rows))
    print("TOP_PERCENTS:", len(top_percents))
    print("### LOOP START ###")

    players = []
    for row, mp in zip(top_rows, top_percents):
        report = row.get("scouting_report", "") or ""

        age_str = extract_from_player_data("Age", report, "0")
        nationality = extract_from_player_data("Nationality", report, "")
        position = extract_from_player_data("Position", report, "")
        current_club = extract_from_player_data("Current club", report, "")
        asking_price = extract_from_player_data("Asking price", report, "")

        age = int(age_str) if age_str.isdigit() else 0

        players.append({
            "player_name": row.get("player_name", ""),
            "age": age,
            "nationality": nationality,
            "position": position,
            "current_club": current_club,
            "asking_price": asking_price,
            "match_percent": float(mp),
        })

        print("APPENDED:", row.get("player_name"), "len(players)=", len(players))

    print("RETURNING PLAYERS:", len(players))
    return {"players": players}
