from pathlib import Path

DATA_PATH = Path(__file__).parents[1] / "data"
VECTOR_DB_PATH = Path(__file__).parent / "knowledge_base"


if __name__ == "__main__":
    print(VECTOR_DB_PATH)
    print(DATA_PATH)
    