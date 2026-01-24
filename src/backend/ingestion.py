from constants import DATA_PATH, VECTOR_DB_PATH
from build_vector_db import setup_vector_db
import time


def ingest_txt_files_to_vector_db(table):
    for file in DATA_PATH.glob("*.txt"):
        with open(file, "r") as f:
            content = f.read()

        player_name = file.stem.replace("_", " ")
        print(f"Loading {player_name} to vector db.")

        table.add([
            {
                "player_name": player_name,
                "filename": file.stem,
                "filepath": str(file),
                "scouting_report": content
            }
        ])

        # print(table.to_pandas()["filename"])
        time.sleep(2)


if __name__ == "__main__":
    vector_db = setup_vector_db(VECTOR_DB_PATH)
    ingest_txt_files_to_vector_db(vector_db["players"])