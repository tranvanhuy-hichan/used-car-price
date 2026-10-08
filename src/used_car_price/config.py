from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data"
RAW_PATH = DATA_DIR / "raw" / "cars.csv"
SAMPLE_PATH = DATA_DIR / "sample" / "sample_cars.csv"
MODEL_DIR = ROOT / "models"
MODEL_PATH = MODEL_DIR / "model.joblib"
METRICS_PATH = MODEL_DIR / "metrics.json"

TARGET = "price_million"          # giá, đơn vị triệu đồng
RAW_COLUMNS = ["brand", "model", "year", "gearbox", "fuel", "province", "origin", "seats", "km", TARGET]
CATEGORICAL = ["brand", "model", "gearbox", "fuel", "province", "origin"]
NUMERIC = ["age", "km", "seats"]
FEATURES = CATEGORICAL + NUMERIC

RANDOM_STATE = 42
TEST_SIZE = 0.2
