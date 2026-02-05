import lancedb
from lancedb.pydantic import LanceModel, Vector
from lancedb.embeddings import get_registry
from constants import DATA_PATH, VECTOR_DB_PATH
from data_models import Player, PlayerProfile


def setup_vector_db(path):
    vector_db = lancedb.connect(uri=path)
    print("connected")

    table = vector_db.create_table("players", schema=PlayerProfile, exist_ok=True)
    print("created table")

    table.create_fts_index("scouting_report", replace=True)
    print("created fts index")

    return vector_db


if __name__ == "__main__":
    setup_vector_db(VECTOR_DB_PATH)