# 3. Mô hình hoá

## Quy trình
1. Chia dữ liệu: 80% train, 20% test (`random_state=42`). Tập test **chỉ dùng một lần** để báo cáo cuối.
2. So sánh 4 mô hình bằng **5-fold cross-validation** trên tập train, độ đo **MAPE** (sai số phần trăm trung bình). Không chọn theo RMSE vì giá có đuôi dài (xe sang tới vài tỉ) nên RMSE bị chi phối bởi vài xe rất đắt.
3. Chọn mô hình có CV MAPE thấp nhất, đánh giá trên tập test.
4. Huấn luyện lại mô hình đó trên toàn bộ dữ liệu, lưu vào `models/model.joblib` để app dùng.

## Mô hình so sánh

| Mô hình | Vai trò | Ghi chú |
|---|---|---|
| Linear Regression | **Baseline** | Cần one-hot và chuẩn hoá. Dễ giải thích |
| Ridge | Tuyến tính có chuẩn hoá L2 | Ổn định hơn khi các biến tương quan |
| Random Forest | Phi tuyến, giảm variance | Bắt được tương tác giữa các thuộc tính |
| Gradient Boosting | Phi tuyến, giảm bias | Thường tốt nhất trên dữ liệu bảng |

## Dự đoán log(giá)
Mọi mô hình được bọc trong `TransformedTargetRegressor` (huấn luyện trên `log1p(giá)`, đổi ngược khi dự đoán). Giá lệch phải, nên sai số theo tỉ lệ phần trăm hợp lý hơn sai số tuyệt đối, và mô hình tuyến tính phù hợp hơn.

## Tiền xử lý (`features.py`)
- Thuộc tính chữ (`brand`, `model`, `gearbox`, `fuel`, `province`, `origin`): **one-hot**; giá trị hiếm (dưới 5 xe) và giá trị chưa từng thấy được gom vào một nhóm "hiếm" (`min_frequency=5`).
- Thuộc tính số (`age`, `km`, `seats`): chuẩn hoá cho mô hình tuyến tính; mô hình cây không cần.

## Kết quả
Sau khi chạy `python scripts/train.py`, kết quả được lưu ở `models/metrics.json` (CV MAPE từng mô hình; MAPE, sai số % trung vị, MAE, RMSE, R² trên test) và hiển thị trong app. **Hãy dán bảng kết quả với dữ liệu thật vào đây** khi có.

| Mô hình | CV RMSE (triệu) |
|---|---|
| Linear Regression | _điền sau khi chạy_ |
| Ridge | _điền sau khi chạy_ |
| Random Forest | _điền sau khi chạy_ |
| Gradient Boosting | _điền sau khi chạy_ |

## Ý tưởng cải tiến
- Tinh chỉnh siêu tham số (`GridSearchCV` hoặc `RandomizedSearchCV`).
- Thêm thuộc tính: dòng xe, năm sản xuất cụ thể, số chủ sở hữu, tình trạng.
- Giải thích mô hình: feature importance, SHAP.
- Phân tích lỗi: nhóm xe nào mô hình dự đoán kém.
- Khoảng dự đoán (quantile regression) thay vì một con số.
