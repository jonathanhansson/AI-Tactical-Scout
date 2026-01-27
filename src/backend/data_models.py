from pydantic import BaseModel, Field
from lancedb.embeddings import get_registry
from lancedb.pydantic import LanceModel, Vector
from dotenv import load_dotenv

load_dotenv()

embedding_model = get_registry().get("gemini-text").create(name="gemini-embedding-001") 
DIM = 3072

class Player(BaseModel):
    player_name: str = Field(description="This is a player name. It consists of first name and last name, e.g. Carl Johnson.")
    age: int = Field(description="Player age must be between 30 and 49.")
    nationality: str = Field(description="E.g. Spain or Italy.")
    position: str = Field(description="A position on the field. You have to choose between center back, striker or goalkeeper")
    preferred_foot: str = Field(description="Two options: 1. Left 2. Right.")
    current_club: str = Field(description="Current club, e.g. FC Barcelona.")
    asking_price: str = Field(description="A price in euro. Always answer in this format, e.g: '30 million euro'.")
    salary_range: str = Field(description="A weekly salary range. E.g. '30.000-50.000 euro/week'.")
    strengths: list[str] = Field(description="List 3 strengths that this player has.")
    weaknesses: list[str] = Field(description="List 3 weaknesses that this player has.")


class RagResponse(BaseModel):
    player_name: str = Field(description="The first and last name of the retrieved player.")
    filepath: str = Field(description="Name the absolute path to the retrieved file.")
    answer: str = Field(description="Answer based on the retrieved file.")


class PlayerProfile(LanceModel):
    player_name: str
    filename: str
    filepath: str
    scouting_report: str = embedding_model.SourceField()
    embedding: Vector(DIM) = embedding_model.VectorField()