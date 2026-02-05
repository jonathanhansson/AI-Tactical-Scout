from pydantic import BaseModel, Field
from lancedb.embeddings import get_registry
from lancedb.pydantic import LanceModel, Vector
from dotenv import load_dotenv

load_dotenv()

embedding_model = get_registry().get("gemini-text").create(name="gemini-embedding-001") 
DIM = 3072

class Player(BaseModel):
    player_name: str = Field(description="This is a player name. It consists of first name and last name, e.g. Carl Johnson.")
    age: int = Field(description="Player age must be between 16 and 35.")
    nationality: str = Field(description="E.g. Spain or Italy.")
    position: str = Field(description="A position on the field. You have to choose between center back, striker or goalkeeper")
    preferred_foot: str = Field(description="Two options: 1. Left 2. Right.")
    current_club: str = Field(description="Current club, e.g. FC Barcelona.")
    asking_price: str = Field(description="A price in euro. Always answer in this format, e.g: '30 million euro'.")
    negotiation_space: int = Field(lt=6, gt=0, description="This is a number between 1 and 5, where 5 means that the selling club are VERY flexible on the 'asking_price' (you can negotiate with them) and 1 means the opposite.")
    salary_range: str = Field(description="A weekly salary range. E.g. '30.000-50.000 euro/week'.")
    salary_negotiation_space: int = Field(lt=6, gt=0, description="This is a number between 1 and 5, where 5 means that the SPECIFIC PLAYER is VERY flexible on the 'salary_range' (they may consider a lower salary than advertised) and 1 means the opposite.")
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


class PlayerShowcase(BaseModel):
    player_name: str = Field(description="Show players name")
    age: int = Field(description="Show players age")
    nationality: str = Field(description="Show players nationality")
    position: str = Field(description="Show players position")
    current_club: str = Field(description="Show players current club")
    asking_price: str = Field(description="Show players asking price")
    match_percent: float = Field(description="How well the player matches the prompt (0-100)")
    

class PlayerShowcaseList(BaseModel):
    players: list[PlayerShowcase] = Field(description="List of 5 players to show")
