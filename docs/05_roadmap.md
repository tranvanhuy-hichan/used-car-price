# 5. Kế hoạch học và phát triển

Dự án này dùng để học machine learning qua thực hành. Mỗi giai đoạn gắn với kiến thức cụ thể.

## Giai đoạn 1: Khung dự án chạy được (đã xong)
- [x] Cấu trúc thư mục, pipeline, web demo, kiểm thử
- [x] Dữ liệu mẫu tổng hợp

## Giai đoạn 2: Dữ liệu thật
- [x] Thu thập dữ liệu (`scripts/crawl_bonbanh.py`)
- [ ] Làm sạch: chuẩn hoá tên hãng, loại ngoại lai, xử lý giá trị thiếu
- [x] Cập nhật `docs/02_data.md` với nguồn và giới hạn

## Giai đoạn 3: Khám phá dữ liệu (EDA), notebook trong `notebooks/`
- [ ] Phân phối giá, mối quan hệ giá với tuổi, km, hãng
- [ ] Thử `log(giá)`

## Giai đoạn 4: Mô hình hoá
- [ ] Hồi quy tuyến tính (baseline): đọc hệ số, vẽ phần dư
- [ ] Ridge, Lasso: so sánh hệ số
- [ ] Cây quyết định, Random Forest, Gradient Boosting
- [ ] Tinh chỉnh siêu tham số
- [ ] Điền bảng kết quả vào `docs/03_modeling.md`

## Giai đoạn 5: Mở rộng theo các thuật toán đã học
- [ ] **Gom cụm (K-Means):** phân khúc thị trường xe (giá rẻ, tầm trung, cao cấp)
- [ ] **PCA:** trực quan hoá dữ liệu thành 2 chiều
- [ ] **Phân lớp (Logistic/SVM/Naive Bayes):** "giá hợp lý hay bị hét cao"
- [ ] **Giải thích mô hình:** feature importance, SHAP

## Giai đoạn 6: Hoàn thiện cho portfolio
- [ ] Ảnh chụp/GIF demo trong README
- [ ] Triển khai app (Streamlit Community Cloud hoặc Hugging Face Spaces)
- [ ] Mục "Hạn chế" trung thực trong README
- [ ] Đưa lên GitHub

## Hướng phát triển xa hơn
Thêm mô tả văn bản và ảnh xe, theo dõi giá theo thời gian, API (FastAPI), Docker hoá.
