# 1. Tổng quan

## Bài toán
Dự đoán **giá bán** (triệu đồng) của một chiếc ô tô cũ từ các thông tin cơ bản. Đây là bài toán **hồi quy** trên dữ liệu dạng bảng.

## Mục tiêu
1. **Học:** áp dụng các thuật toán đã học (hồi quy tuyến tính, Ridge, Random Forest, Gradient Boosting) trên một bài toán có ý nghĩa thực tế.
2. **Sản phẩm:** một ứng dụng web nhỏ, nhập thông tin xe và nhận giá gợi ý.
3. **Portfolio:** repo gọn gàng, có tài liệu, chạy lại được.

## Phạm vi
- **Trong phạm vi:** xe ô tô cũ đăng bán trên bonbanh.com, 9 thuộc tính đầu vào, dự đoán một giá trị (giá chào bán).
- **Ngoài phạm vi (hiện tại):** ảnh xe, mô tả văn bản, giá theo thời gian, xe máy.

## Độ đo thành công
- **MAE** (sai số tuyệt đối trung bình, triệu đồng): dễ hiểu nhất với người dùng.
- **RMSE:** phạt nặng các dự đoán sai lớn, dùng để chọn mô hình.
- **R²:** tỉ lệ biến thiên của giá mà mô hình giải thích được.
- Mục tiêu đặt ra khi có dữ liệu thật: MAE nhỏ hơn khoảng 10% giá trung vị. Cần cập nhật sau khi thấy phân phối giá thật.

## Quyết định thiết kế
- Dùng `Pipeline` để tiền xử lý và mô hình đi liền nhau, tránh rò rỉ dữ liệu khi cross-validation.
- Luôn có **baseline** (hồi quy tuyến tính) để biết mô hình phức tạp hơn thực sự tốt hơn bao nhiêu.
- Streamlit cho giao diện vì chỉ cần Python, không cần frontend riêng.
