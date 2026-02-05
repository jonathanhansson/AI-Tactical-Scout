from pathlib import Path
import os

CURRENT_FILE = Path(__file__).resolve()

if os.path.exists("/app"):
    DATA_PATH = Path("/app/data")
else:
    DATA_PATH = CURRENT_FILE.parents[2] / "data"

VECTOR_DB_PATH = Path(__file__).parents[1] / "knowledge_base"


if __name__ == "__main__":
    print(VECTOR_DB_PATH)
    print(DATA_PATH)
    