import joblib
import pandas as pd

from .config import FEATURES, MODEL_PATH

_model = None


def load_model(path=MODEL_PATH):
    global _model
    if _model is None:
        if not path.exists():
            raise FileNotFoundError(f"Chưa có mô hình tại {path}. Chạy `python scripts/train.py` trước.")
        _model = joblib.load(path)
    return _model


def predict_price(brand: str, model: str, gearbox: str, fuel: str, province: str,
                  origin: str, age: int, km: int, seats: int) -> float:
    """Trả về giá dự đoán (triệu đồng)."""
    row = pd.DataFrame([{"brand": brand, "model": model, "gearbox": gearbox, "fuel": fuel,
                         "province": province, "origin": origin, "age": age, "km": km, "seats": seats}])[FEATURES]
    return float(load_model().predict(row)[0])
