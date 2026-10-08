from datetime import date

import pandas as pd

from .config import FEATURES, RAW_PATH, SAMPLE_PATH, TARGET


def load_data(path=None) -> pd.DataFrame:
    """Đọc dữ liệu: ưu tiên data/raw/cars.csv, nếu chưa có thì dùng dữ liệu mẫu."""
    path = path or (RAW_PATH if RAW_PATH.exists() else SAMPLE_PATH)
    if not path.exists():
        raise FileNotFoundError(
            f"Không thấy {path}. Chạy `python scripts/crawl_bonbanh.py` hoặc "
            "`python scripts/generate_sample_data.py` để có dữ liệu.")
    return clean(pd.read_csv(path))


def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Làm sạch: tạo `age` từ `year`, bỏ dòng trùng/thiếu, loại giá trị vô lý và ngoại lai giá."""
    df = df.copy()
    if "age" not in df.columns:
        df["age"] = date.today().year - df["year"]
    if "listing_id" in df.columns:
        df = df.drop_duplicates(subset="listing_id")
    df = df.drop_duplicates().dropna(subset=FEATURES + [TARGET])
    df = df[(df[TARGET] > 0) & (df["km"] >= 0) & (df["age"] >= 0) & (df["seats"] > 0)]
    # Loại ngoại lai giá cực đoan (tin nhập nhầm đơn vị...): ngoài 0,5% hai đầu
    lo, hi = df[TARGET].quantile([0.005, 0.995])
    df = df[df[TARGET].between(lo, hi)]
    for c in ["brand", "model", "gearbox", "fuel", "province", "origin"]:
        df[c] = df[c].astype(str).str.strip()
    return df.reset_index(drop=True)
