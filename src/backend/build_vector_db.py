import lancedb
from constants import DATA_PATH, VECTOR_DB_PATH
from data_models import Player


def setup_vector_db(path):
    vector_db = lancedb.connect(uri=path)
    vector_db.create_table("players", schema=Player, exist_ok=True)

    return vector_db


if __name__ == "__main__":
    setup_vector_db(VECTOR_DB_PATH)