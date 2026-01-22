import lancedb
from lancedb.pydantic import LanceModel, Vector
from lancedb.embeddings import get_registry
from constants import DATA_PATH, VECTOR_DB_PATH
from data_models import Player, PlayerProfile


def setup_vector_db(path):
    vector_db = lancedb.connect(uri=path)
    print("connected")
    vector_db.create_table("players", schema=PlayerProfile, exist_ok=True)
    print("created table")

    return vector_db


if __name__ == "__main__":
    setup_vector_db(VECTOR_DB_PATH)