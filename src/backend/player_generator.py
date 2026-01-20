from data_models import Player
from pydantic_ai import Agent
from dotenv import load_dotenv
import os
import asyncio
import random

load_dotenv()

generator_agent = Agent(
    model="google-gla:gemini-2.5-flash",
    output_type=Player, # using 'output_type' instead of 'result_type' to comply with latest documentation. Read more here: https://ai.pydantic.dev/output/
    system_prompt=(
        "You are an expert football (soccer) scout.",
        "Based on a user prompt, you should generate a random player.",
        "It should NOT be a real player, instead come up with a new player that doesn't exist in the real world."
    )
)


writer_agent = Agent(
    model="google-gla:gemini-2.5-flash",
    system_prompt=(
        "You are a professional and experienced football (soccer) agent.",
        "With the data provided, you should write a passionate scout report.",
        "Focus on playstyle, how strengths/weaknesses manifest on the pitch and future potential.",
        "Do NOT use bullet points. Write in prose (paragraphs)."
    )
)


async def create_player_file(prompt: str):
    print("1. Running player generator agent")
    generator_result = await generator_agent.run(prompt)

    player = generator_result.output

    print(f"2. Writing report for {player.player_name}")
    report_result = await writer_agent.run(f"Write a report based on this data {player}")
    report_text = report_result.output

    file_content = f"""
    SCOUTING REPORT FOR {player.player_name}
    ---------------------------------------------------------
    {report_text}
    ---------------------------------------------------------
    PLAYER DATA
    ---------------------------------------------------------
    Name: {player.player_name}
    Age: {player.age}
    Nationality: {player.nationality}
    Position: {player.position}
    Preferred foot: {player.preferred_foot}
    Current club: {player.current_club}
    Asking price: {player.asking_price}
    Salary range: {player.salary_range}
    Strengths: {', '.join(player.strengths)}
    Weaknesses: {', '.join(player.weaknesses)}
    ---------------------------------------------------------
    """

    filename = player.player_name.replace(" ", "_")
    filepath = f"data/{filename}.txt"
    os.makedirs("data", exist_ok=True)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(file_content)

    return filepath


if __name__ == "__main__":
    seed = random.randint(1, 1000)
    

    prompt = f"Generate a player. Random seed: {seed}. Make sure the name is random."

    filepath = asyncio.run(create_player_file(prompt))
    print(f"Player saved to {filepath}")