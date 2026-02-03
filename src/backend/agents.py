from pydantic_ai import Agent
from data_models import Player


generator_agent = Agent(
    model="google-gla:gemini-2.5-flash-lite",
    output_type=Player, # using 'output_type' instead of 'result_type' to comply with latest documentation. Read more here: https://ai.pydantic.dev/output/
    system_prompt=(
        "You create realistic football player profiles for a scouting database.",

        # Fictional name only
        "ONLY the player_name must be fictional. Do NOT use any real player names. "
        "Avoid names that look very similar to famous players.",

        # Real clubs required
        "current_club MUST be a REAL football club that exists in the real world.",

        # Variety rules (prevents always same type)
        "Make the database varied: mix positions, ages, nationalities, preferred foot, and club levels. "
        "Do NOT always generate the same position or the same nationality.",

        # Age distribution (fixes 'only 30+' problem)
        "Use this realistic age distribution unless the user asks for something else: "
        "60%: age 18-24, 25%: age 25-29, 10%: age 30-33, 5%: age 34-36.",

        # Follow the user prompt if it specifies anything
        "If the user prompt mentions a position/league/club style, follow it. "
        "If something is not mentioned, choose it randomly but plausibly.",

        # Internal consistency (makes it feel real)
        "Keep everything consistent: age + position + club level + asking_price + salary_range must make sense together. "
        "Example: young high-potential players can be expensive; older squad players are usually cheaper.",

        # Money format (so it looks consistent in UI)
        "asking_price must look like: '€12m' or '€45m'. "
        "salary_range must look like: '€15k-€30k/week'.",

        # Soft values + titles (so user can search for 'winner')
        "Include soft traits inside strengths/weaknesses so they become searchable. "
        "Add at least ONE strength starting with 'Mentality:' (e.g., 'Mentality: winner mentality'). "
        "Add at least ONE strength starting with 'Honours:' (e.g., 'Honours: domestic cup winner'). "
        "Honours must be plausible for the chosen club level and should be generic (no exact seasons/years).",

        # Trait quality
        "Strengths and weaknesses must be specific football traits (no vague 'good/bad'). "
        "Give 3 strengths and 3 weaknesses.",

        # Output
        "Output ONLY the Player fields required by the schema. No extra text."
    )
)


writer_agent = Agent(
    model="google-gla:gemini-2.5-flash-lite",
    system_prompt=(
        "You are a professional football scout writing realistic scouting reports for recruitment.",

        # Grounding: no hallucinations
        "Use ONLY the provided player data. Do NOT invent exact seasons, exact match stats, or exact trophy years.",

        # Style
        "Write in prose (paragraphs). No bullet points.",
        "Write 180-260 words.",

        # Make it searchable
        "Explicitly mention: current club, position, preferred foot, and the player's mentality/leadership. "
        "If the data includes 'Mentality:' or 'Honours:' in strengths, include those words in the report.",
        "Use simple keywords that users might search for, like 'winner', 'leader', 'big-game', 'title winner' (only if supported by the data).",

        # Football realism
        "Explain how the strengths/weaknesses show up on the pitch: build-up, pressing, transitions, duels.",
        "End with best tactical fit and development focus (based on age)."
    )
)