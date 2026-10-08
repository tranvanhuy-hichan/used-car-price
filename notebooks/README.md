# Notebooks học qua dự án

Học theo thứ tự. Mỗi notebook có mục tiêu, câu hỏi suy nghĩ và **bài tập cuối bài**. Hãy tự dự đoán kết quả trước khi chạy từng cell.

| # | Notebook | Bạn học được gì |
|---|---|---|
| 01 | `01_kham_pha_du_lieu` | Làm sạch từng bước và đo tác động, phân phối giá, vì sao dùng log, thiên lệch do bỏ tin thiếu km |
| 02 | `02_hoi_quy_tuyen_tinh` | Baseline, tuyến tính trên giá thô và log(giá), phần dư, diễn giải hệ số theo %, đa cộng tuyến, Ridge/Lasso |
| 03 | `03_mo_hinh_cay` | Overfitting của cây đơn, Random Forest, vì sao Gradient Boosting mặc định bị underfit |
| 04 | `04_danh_gia_va_tinh_chinh` | Chọn độ đo, tìm tham số ngẫu nhiên, phân tích lỗi theo nhóm, learning curve, khoảng dự đoán, lưu mô hình |
| 05 | `05_giai_thich_mo_hinh` | Độ quan trọng (impurity và permutation), PDP/ICE, phân tích "nếu thay đổi một yếu tố" |
| 06 | `06_phan_cum_va_pca` | K-Means phân khúc thị trường, PCA, vì sao PCA không giúp dự đoán giá, phát hiện tin bất thường |
| 07 | `07_phan_lop_phan_khuc_xe` | Logistic, Naïve Bayes, SVM, Random Forest, chọn ngưỡng, odds ratio |

## Chạy
```bash
pip install -r requirements.txt jupyter
jupyter lab notebooks/
```
Các notebook đọc `data/raw/cars.csv` (chạy `python scripts/crawl_bonbanh.py` trước), nếu chưa có thì dùng dữ liệu mẫu tổng hợp. Kết quả trong notebook đã lưu sẵn từ dữ liệu thu thập ngày 08/10/2026; số liệu sẽ khác khi bạn thu thập lại.
