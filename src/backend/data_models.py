from pydantic import BaseModel, Field
from lancedb.embeddings import get_registry
from lancedb.pydantic import LanceModel, Vector
from dotenv import load_dotenv

load_dotenv()

embedding_model = get_registry().get("gemini-text").create(name="gemini-embedding-001")

class Player(BaseModel):
    player_name: str = Field(description="This is a player name. It consists of surname and last name, e.g. Carl Johnson.")
    age: int = Field(lt=50, gt=15, description="Player age. A whole number between 16 and 49. Make sure to make it random.")
    nationality: str = Field(description="E.g. Spain or Italy.")
    position: str = Field(description="A position on the field. Here are some examples: 'Striker', 'Central Midfielder', 'Wing Back'.")
    preferred_foot: str = Field(description="Two options: 1. Left 2. Right.")
    current_club: str = Field(description="Current club, e.g. FC Barcelona.")
    asking_price: str = Field(description="A price in euro. Always answer in this format, e.g: '30 million euro'.")
    salary_range: str = Field(description="A weekly salary range. E.g. '30.000-50.000 euro/week'.")
    strengths: list[str] = Field(description="List 3 strengths that this player has.")
    weaknesses: list[str] = Field(description="List 3 weaknesses that this player has.")