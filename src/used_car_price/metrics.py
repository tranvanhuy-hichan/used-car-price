import numpy as np
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error, mean_squared_error, r2_score


def evaluate(y_true, y_pred) -> dict:
    """Các độ đo hồi quy dùng chung. Sai số % phù hợp hơn RMSE khi giá có đuôi dài."""
    y_true, y_pred = np.asarray(y_true, float), np.asarray(y_pred, float)
    return {
        "MAPE": float(mean_absolute_percentage_error(y_true, y_pred)),
        "sai_so_%_trung_vi": float(np.median(np.abs(y_pred - y_true) / y_true)),
        "MAE": float(mean_absolute_error(y_true, y_pred)),
        "RMSE": float(np.sqrt(mean_squared_error(y_true, y_pred))),
        "R2": float(r2_score(y_true, y_pred)),
    }
