from pydantic import BaseModel, Field
from lancedb.embeddings import get_registry
from lancedb.pydantic import LanceModel, Vector
from dotenv import load_dotenv

load_dotenv()

embedding_model = get_registry().get("gemini-text").create(name="gemini-embedding-001")

class Player(BaseModel):
    player_name: str = Field(description="This is a player name. It consists of surname and last name, e.g. Carl Johnson")
    age: int = Field(lt=50, gt=15, description="Player age. A whole number between 16 and 49.")
    nationality: str = Field(description="E.g. Spain or Italy.")
    preferred_foot: str = Field(description="Two options: 1. Left 2. Right.")
    current_club: str = Field(description="Current club, e.g. FC Barcelona.")