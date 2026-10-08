"""Ứng dụng web đơn giản: nhập thông tin xe -> giá gợi ý.

Chạy:  streamlit run app/streamlit_app.py
"""
import json
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from used_car_price.config import METRICS_PATH, MODEL_PATH, RAW_PATH  # noqa: E402
from used_car_price.data import load_data  # noqa: E402
from used_car_price.predict import predict_price  # noqa: E402

st.set_page_config(page_title="Dự đoán giá ô tô cũ", page_icon="🚗")
st.title("🚗 Dự đoán giá ô tô cũ")
st.caption("Nhập thông tin xe để nhận giá gợi ý. Đây chỉ là ước lượng tham khảo từ mô hình học máy.")

if not MODEL_PATH.exists():
    st.error("Chưa có mô hình. Chạy `python scripts/train.py` trước rồi tải lại trang.")
    st.stop()


@st.cache_data
def load_df():
    return load_data()


df = load_df()
col1, col2 = st.columns(2)
brand = col1.selectbox("Hãng xe", sorted(df["brand"].unique()))
model = col1.selectbox("Dòng xe", sorted(df.loc[df["brand"] == brand, "model"].unique()))
gearbox = col1.selectbox("Hộp số", sorted(df["gearbox"].unique()))
fuel = col1.selectbox("Nhiên liệu", sorted(df["fuel"].unique()))
origin = col2.selectbox("Xuất xứ", sorted(df["origin"].unique()))
province = col2.selectbox("Tỉnh / thành phố", sorted(df["province"].unique()))
age = col2.slider("Tuổi xe (năm)", 0, 25, 5)
km = col2.number_input("Số km đã đi", 0, 500_000, 60_000, step=5_000)
seats = col2.selectbox("Số chỗ", sorted(df["seats"].unique()), index=0)

if st.button("Dự đoán giá", type="primary"):
    price = predict_price(brand, model, gearbox, fuel, province, origin, age, int(km), int(seats))
    st.metric("Giá gợi ý", f"{price:,.0f} triệu đồng")

if METRICS_PATH.exists():
    m = json.loads(METRICS_PATH.read_text(encoding="utf-8"))
    with st.expander("Thông tin mô hình"):
        st.write(f"Mô hình: **{m['best_model']}**")
        st.write(f"Sai số phần trăm trung vị: **{m['test_median_ape']:.1%}** | MAPE: **{m['test_mape']:.1%}** | "
                 f"MAE: **{m['test_mae']:.0f} triệu** | R²: **{m['test_r2']:.3f}**")
        src = "dữ liệu thật thu thập từ bonbanh.com" if RAW_PATH.exists() else "dữ liệu mẫu tổng hợp (chưa phải dữ liệu thật)"
        st.write(f"Nguồn dữ liệu huấn luyện: {src}, {m['n_rows']} dòng.")
        st.caption("Giá trong tin rao là giá chào bán, thường cao hơn giá giao dịch cuối cùng.")
