"""Huấn luyện, so sánh mô hình bằng cross-validation, lưu mô hình tốt nhất.

Chạy:  python -m used_car_price.train      (hoặc  python scripts/train.py)
"""
import json

import joblib
import numpy as np
from sklearn.compose import TransformedTargetRegressor
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error, mean_squared_error, r2_score
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.pipeline import Pipeline

from .config import FEATURES, METRICS_PATH, MODEL_DIR, MODEL_PATH, RANDOM_STATE, TARGET, TEST_SIZE
from .data import load_data
from .features import build_preprocessor


def log_target(pipe: Pipeline) -> TransformedTargetRegressor:
    """Dự đoán log(giá) rồi đổi ngược: giá lệch phải, sai số theo tỉ lệ phần trăm hợp lý hơn."""
    return TransformedTargetRegressor(regressor=pipe, func=np.log1p, inverse_func=np.expm1)


def candidates() -> dict:
    return {
        "linear_regression (baseline)": log_target(Pipeline([("prep", build_preprocessor()), ("model", LinearRegression())])),
        "ridge": log_target(Pipeline([("prep", build_preprocessor()), ("model", Ridge(alpha=1.0))])),
        "random_forest": log_target(Pipeline([("prep", build_preprocessor(False)),
                                              ("model", RandomForestRegressor(300, random_state=RANDOM_STATE, n_jobs=-1))])),
        "gradient_boosting": log_target(Pipeline([("prep", build_preprocessor(False)),
                                                  ("model", GradientBoostingRegressor(n_estimators=800, learning_rate=0.05, max_depth=4,
                                                                                  subsample=0.8, random_state=RANDOM_STATE))])),
    }


def main() -> None:
    df = load_data()
    X, y = df[FEATURES], df[TARGET]
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE)
    print(f"Dữ liệu: {len(df)} dòng | train={len(X_tr)} test={len(X_te)}\n")

    results = {}
    for name, pipe in candidates().items():
        # Chọn mô hình theo sai số phần trăm (MAPE): giá lệch phải, RMSE bị chi phối bởi vài xe rất đắt
        cv_mape = -cross_val_score(pipe, X_tr, y_tr, cv=5, scoring="neg_mean_absolute_percentage_error").mean()
        results[name] = float(cv_mape)
        print(f"{name:30s} CV MAPE = {cv_mape:6.1%}")

    best_name = min(results, key=results.get)
    best = candidates()[best_name].fit(X_tr, y_tr)
    pred = best.predict(X_te)
    metrics = {
        "best_model": best_name,
        "cv_mape": results,
        "test_mape": float(mean_absolute_percentage_error(y_te, pred)),
        "test_median_ape": float(np.median(np.abs(pred - y_te) / y_te)),
        "test_rmse": float(np.sqrt(mean_squared_error(y_te, pred))),
        "test_mae": float(mean_absolute_error(y_te, pred)),
        "test_r2": float(r2_score(y_te, pred)),
        "n_rows": int(len(df)),
    }
    print(f"\nMô hình tốt nhất: {best_name}")
    print(f"Test: MAPE={metrics['test_mape']:.1%} | sai số % trung vị={metrics['test_median_ape']:.1%} | "
          f"MAE={metrics['test_mae']:.1f} triệu | RMSE={metrics['test_rmse']:.1f} | R²={metrics['test_r2']:.3f}")

    # Huấn luyện lại trên toàn bộ dữ liệu để dùng cho app
    final = candidates()[best_name].fit(X, y)
    MODEL_DIR.mkdir(exist_ok=True)
    joblib.dump(final, MODEL_PATH)
    METRICS_PATH.write_text(json.dumps(metrics, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Đã lưu mô hình: {MODEL_PATH}")


if __name__ == "__main__":
    main()
