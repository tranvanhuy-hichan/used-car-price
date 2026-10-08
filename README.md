# Used Car Price: Dự đoán giá ô tô cũ

Ứng dụng Python đơn giản dự đoán giá ô tô cũ (triệu đồng) từ hãng, hộp số, nhiên liệu, tỉnh/thành, tuổi xe và số km. Dự án dùng để học và thực hành quy trình machine learning với dữ liệu dạng bảng, từ làm sạch dữ liệu, so sánh mô hình, đến web demo.

> **Dữ liệu:** thu thập từ các trang danh sách của [bonbanh.com](https://bonbanh.com) bằng `scripts/crawl_bonbanh.py`. Đây là **giá chào bán**, không phải giá giao dịch cuối. Xem [docs/02_data.md](docs/02_data.md) về nguồn, giới hạn và cách thu thập có trách nhiệm.

## Cài đặt và chạy

```bash
# 1. Tạo môi trường và cài thư viện
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 2. Thu thập dữ liệu thật vào data/raw/cars.csv (~10 phút cho 200 trang)
python scripts/crawl_bonbanh.py --pages 200
#    (hoặc tạo dữ liệu mẫu tổng hợp để chạy thử: python scripts/generate_sample_data.py)

# 3. Huấn luyện, so sánh mô hình, lưu mô hình tốt nhất vào models/
python scripts/train.py

# 4. Chạy ứng dụng web
streamlit run app/streamlit_app.py

# 5. Chạy kiểm thử
pytest
```

## Cấu trúc thư mục

```
used-car-price/
├── README.md
├── requirements.txt
├── .gitignore
├── app/
│   └── streamlit_app.py        # Web demo: nhập thông tin xe -> giá gợi ý
├── data/
│   ├── raw/                    # Dữ liệu thật (cars.csv), KHÔNG đưa lên git
│   ├── processed/              # Dữ liệu đã xử lý, KHÔNG đưa lên git
│   └── sample/                 # Dữ liệu mẫu tổng hợp (đưa lên git được)
├── docs/                       # Tài liệu dự án
│   ├── 01_overview.md          # Mục tiêu, phạm vi
│   ├── 02_data.md              # Dữ liệu: cột, nguồn, cách thu thập
│   ├── 03_modeling.md          # Mô hình, đánh giá, kết quả
│   ├── 04_usage.md             # Hướng dẫn chạy và phát triển
│   └── 05_roadmap.md           # Kế hoạch học và phát triển tiếp
├── models/                     # Mô hình đã huấn luyện (không đưa lên git)
├── notebooks/                  # 7 notebook học tập theo dự án (xem notebooks/README.md)
├── scripts/
│   ├── crawl_bonbanh.py        # Thu thập dữ liệu từ bonbanh.com
│   ├── generate_sample_data.py # Tạo dữ liệu mẫu tổng hợp
│   └── train.py                # Điểm vào để huấn luyện
├── src/used_car_price/         # Mã nguồn chính
│   ├── config.py               # Đường dẫn, tên cột, hằng số
│   ├── data.py                 # Đọc và làm sạch dữ liệu
│   ├── features.py             # Tiền xử lý thuộc tính (ColumnTransformer)
│   ├── train.py                # So sánh mô hình, lưu mô hình tốt nhất
│   └── predict.py              # Nạp mô hình và dự đoán
└── tests/
    └── test_pipeline.py        # Kiểm thử cơ bản
```

## Notebook học tập
Bộ 7 notebook trong [notebooks/](notebooks/README.md) đi từ khám phá dữ liệu, hồi quy tuyến tính, mô hình cây, đánh giá và tinh chỉnh, giải thích mô hình, đến gom cụm/PCA và phân lớp, trên chính dữ liệu của dự án.

## Kết quả hiện tại
Trên dữ liệu thu thập từ bonbanh.com (2.849 tin sau làm sạch), Random Forest cho sai số phần trăm trung vị khoảng **6,8%** và MAPE khoảng 11,3% trên tập test. Gradient Boosting sau khi tinh chỉnh (notebook 04) đạt MAPE khoảng 10,8%. Đây là sai số trên **giá chào bán**, không phải giá giao dịch.

## Công nghệ
Python, pandas, scikit-learn, Streamlit, pytest. Crawler chỉ dùng thư viện chuẩn (`urllib`, `re`).

## Tài liệu
Xem thư mục [docs/](docs/).
