from pydantic_ai import Agent
from data_models import Player


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