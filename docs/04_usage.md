# 4. Hướng dẫn sử dụng và phát triển

## Yêu cầu
Python 3.10 trở lên.

## Cài đặt
```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Các lệnh thường dùng

| Việc | Lệnh |
|---|---|
| Thu thập dữ liệu thật | `python scripts/crawl_bonbanh.py --pages 200` |
| Tạo dữ liệu mẫu tổng hợp | `python scripts/generate_sample_data.py` |
| Huấn luyện và lưu mô hình | `python scripts/train.py` |
| Chạy web app | `streamlit run app/streamlit_app.py` |
| Chạy kiểm thử | `pytest` |

Thứ tự lần đầu: thu thập dữ liệu, huấn luyện, chạy app. App yêu cầu đã có `models/model.joblib`.

## Dùng mô hình từ code Python
```python
import sys; sys.path.insert(0, "src")
from used_car_price.predict import predict_price

price = predict_price(brand="Toyota", model="Fortuner", gearbox="tự động", fuel="xăng",
                      province="Hà Nội", origin="trong nước", age=5, km=60000, seats=7)
print(f"{price:.0f} triệu đồng")
```

## Luồng mã nguồn
```
data/raw/cars.csv ◄── scripts/crawl_bonbanh.py
        │
        ▼
    data.py (đọc + làm sạch) ──► train.py (so sánh, chọn, lưu)
                                                         │
                                          models/model.joblib + metrics.json
                                                         │
                          predict.py (nạp mô hình) ◄─────┘
                                  ▲
                      app/streamlit_app.py (giao diện)
```

## Thêm một thuộc tính mới
1. Thêm cột vào dữ liệu.
2. Thêm tên cột vào `CATEGORICAL` hoặc `NUMERIC` trong `config.py`.
3. Thêm đầu vào tương ứng trong `app/streamlit_app.py` và tham số trong `predict.py`.
4. Chạy lại `python scripts/train.py`.

## Thêm một mô hình mới
Thêm một mục vào hàm `candidates()` trong `src/used_car_price/train.py`. Mô hình nào có CV MAPE thấp nhất sẽ tự được chọn.

## Xử lý sự cố
- **"Chưa có mô hình"** khi mở app: chạy `python scripts/train.py` trước.
- **`ModuleNotFoundError: used_car_price`**: chạy lệnh từ thư mục gốc dự án; các script đã tự thêm `src/` vào đường dẫn.
- **Dự đoán lạ với hãng/tỉnh mới**: mô hình chưa thấy giá trị đó khi huấn luyện, nên nó bị bỏ qua; cần thêm dữ liệu.

## Tuỳ chọn của crawler
```bash
python scripts/crawl_bonbanh.py --pages 200 --start 1 --delay 2.0
```
- `--pages`: số trang cần lấy (mỗi trang tối đa 20 tin).
- `--start`: trang bắt đầu (để lấy tiếp các trang sau).
- `--delay`: giây nghỉ tối thiểu giữa các yêu cầu. Đừng đặt thấp hơn 2.
- Chạy lại nhiều lần được: tin đã có (theo `listing_id`) sẽ không bị lặp.
