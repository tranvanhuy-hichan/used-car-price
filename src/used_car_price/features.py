from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from .config import CATEGORICAL, NUMERIC


def build_preprocessor(scale_numeric: bool = True) -> ColumnTransformer:
    """Biến đổi thuộc tính. Mô hình tuyến tính cần chuẩn hoá, mô hình cây thì không bắt buộc."""
    num = StandardScaler() if scale_numeric else "passthrough"
    return ColumnTransformer([
        ("cat", OneHotEncoder(handle_unknown="infrequent_if_exist", min_frequency=5), CATEGORICAL),
        ("num", num, NUMERIC),
    ])
