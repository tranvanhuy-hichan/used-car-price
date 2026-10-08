"""Tạo dữ liệu MẪU TỔNG HỢP (không phải dữ liệu thật) để chạy thử quy trình khi chưa có dữ liệu thật.

Dữ liệu thật: chạy `python scripts/crawl_bonbanh.py` (lưu vào data/raw/cars.csv).
"""
import sys
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from used_car_price.config import SAMPLE_PATH  # noqa: E402

rng = np.random.default_rng(0)
N = 1500
cars = {"Toyota": (["Vios", "Camry", "Fortuner"], 1.10), "Honda": (["City", "Civic", "CR-V"], 1.05),
        "Mazda": (["3", "CX5", "CX8"], 0.95), "Hyundai": (["Accent", "Creta", "Santafe"], 0.90),
        "Kia": (["Morning", "Seltos", "Carnival"], 0.88), "VinFast": (["VF6", "VF8", "Lux A"], 0.85),
        "Ford": (["Ranger", "Everest", "EcoSport"], 0.82), "Mercedes Benz": (["C200", "E300", "GLC"], 2.2)}
provinces = ["Hà Nội", "Hồ Chí Minh", "Đà Nẵng", "Cần Thơ", "Hải Phòng"]

brand = rng.choice(list(cars), N, p=[.22, .17, .12, .15, .13, .08, .08, .05])
model = np.array([rng.choice(cars[b][0]) for b in brand])
age = rng.integers(0, 15, N)
year = date.today().year - age
km = np.clip(age * rng.normal(12000, 4000, N) + rng.normal(3000, 2000, N), 500, None).round(-2).astype(int)
gearbox = rng.choice(["tự động", "số sàn"], N, p=[.65, .35])
fuel = rng.choice(["xăng", "dầu", "hybrid", "điện"], N, p=[.78, .12, .06, .04])
province = rng.choice(provinces, N)
origin = rng.choice(["trong nước", "nhập khẩu"], N, p=[.7, .3])
seats = rng.choice([5, 7], N, p=[.7, .3])

price = 650 * np.array([cars[b][1] for b in brand]) * np.exp(-0.085 * age) - 0.0009 * km
price *= np.where(gearbox == "số sàn", 0.93, 1.0) * np.where(fuel == "hybrid", 1.08, 1.0) * np.where(fuel == "điện", 1.12, 1.0)
price *= np.where(origin == "nhập khẩu", 1.1, 1.0) * np.where(seats == 7, 1.08, 1.0)
price = np.clip(price * rng.normal(1, 0.06, N), 80, None).round(0)

df = pd.DataFrame({"brand": brand, "model": model, "year": year, "gearbox": gearbox, "fuel": fuel,
                   "province": province, "origin": origin, "seats": seats, "km": km, "price_million": price})
SAMPLE_PATH.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(SAMPLE_PATH, index=False)
print(f"Đã tạo {len(df)} dòng -> {SAMPLE_PATH}")
