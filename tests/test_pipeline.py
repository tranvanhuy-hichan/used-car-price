import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from used_car_price.config import FEATURES, TARGET  # noqa: E402
from used_car_price.data import clean  # noqa: E402
from used_car_price.train import candidates  # noqa: E402


def make_df(n=60):
    return pd.DataFrame({
        "brand": ["Toyota", "Honda", "Kia", "Toyota"] * (n // 4),
        "model": ["Vios", "City", "Seltos", "Camry"] * (n // 4),
        "year": [2024 - (i % 15) for i in range(n)],
        "gearbox": ["tự động", "số sàn"] * (n // 2),
        "fuel": ["xăng", "dầu"] * (n // 2),
        "province": ["Hà Nội", "Hồ Chí Minh"] * (n // 2),
        "origin": ["trong nước", "nhập khẩu"] * (n // 2),
        "seats": [5, 7] * (n // 2),
        "km": [10000 * (i % 12 + 1) for i in range(n)],
        TARGET: [800 - 20 * (i % 15) + i for i in range(n)],
    })


def test_clean_removes_invalid_rows_and_adds_age():
    df = make_df()
    df.loc[0, "km"] = -5
    df.loc[1, TARGET] = None
    out = clean(df)
    assert "age" in out.columns
    assert len(out) <= len(df) - 2


def test_all_candidates_fit_and_predict():
    df = clean(make_df())
    for name, pipe in candidates().items():
        pipe.fit(df[FEATURES], df[TARGET])
        assert pipe.predict(df[FEATURES].head(3)).shape == (3,), name
