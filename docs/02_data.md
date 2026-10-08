# 2. Dữ liệu

## Nguồn
Các trang danh sách ô tô cũ của **bonbanh.com** (`https://bonbanh.com/oto/page,N`). Script: [`scripts/crawl_bonbanh.py`](../scripts/crawl_bonbanh.py).

### Vì sao chọn nguồn này
- `robots.txt` của bonbanh.com cho phép (`Allow: /`) và không có hạn chế về AI.
- Chợ Tốt khai báo `Content-Signal: ai-train=no` trong `robots.txt` (không cho dùng dữ liệu để huấn luyện mô hình), nên dự án **không** thu thập từ Chợ Tốt.
- Trang danh sách đã chứa gần đủ thông tin, không cần vào từng tin, nên số yêu cầu gửi tới máy chủ ít.

### Cách thu thập có trách nhiệm
- Nghỉ 2 - 3 giây giữa các yêu cầu, dừng ngay khi gặp HTTP 403/429.
- Chỉ lưu thông tin về xe. **Không lưu** tên người bán, số điện thoại, ảnh, mô tả tự do.
- Dữ liệu thô nằm trong `data/raw/` (đã `.gitignore`), không đưa lên GitHub.
- Kiểm tra lại điều khoản sử dụng của trang trước khi thu thập lại hoặc dùng cho mục đích khác ngoài học tập.

## Lược đồ `data/raw/cars.csv`

| Cột | Kiểu | Ý nghĩa | Ví dụ |
|---|---|---|---|
| `listing_id` | chuỗi | Mã tin (dùng để loại trùng) | 7024368 |
| `brand` | chữ | Hãng xe | Toyota |
| `model` | chữ | Dòng xe (từ đầu tiên sau tên hãng) | Fortuner |
| `year` | số nguyên | Năm sản xuất | 2019 |
| `gearbox` | chữ | Hộp số | tự động / số sàn |
| `fuel` | chữ | Nhiên liệu | xăng / dầu / điện / hybrid |
| `province` | chữ | Tỉnh / thành phố | Hà Nội |
| `origin` | chữ | Xuất xứ | trong nước / nhập khẩu |
| `seats` | số nguyên | Số chỗ ngồi | 7 |
| `km` | số nguyên | Số km đã đi | 60000 |
| `price_million` | số | **Giá chào bán (nhãn)**, triệu đồng | 520 |
| `crawled_at` | ngày | Ngày thu thập | 2026-10-08 |

`age` (tuổi xe) được tính trong `data.py` bằng `năm hiện tại - year`.

## Giới hạn của dữ liệu
- **Giá chào bán, không phải giá giao dịch.** Thường cao hơn giá bán thực tế, nên mô hình dự đoán giá niêm yết.
- **Thiếu số km:** mô tả trong trang danh sách bị cắt nên khoảng 11% tin không có số km. Các tin này bị loại khi làm sạch vì km là thuộc tính quan trọng (quan sát trên dữ liệu thu được: tin thiếu km là xe cũ hơn và rẻ hơn, nên bỏ chúng làm tập huấn luyện nghiêng về xe đời mới; xem notebook 01). Muốn lấy thêm cần vào trang chi tiết từng tin (nhiều yêu cầu hơn, cần cân nhắc).
- **Chỉ các tin đang đăng** tại thời điểm thu thập; tin gần đây nhiều hơn tin cũ, thị trường thay đổi theo thời gian.
- **Tên dòng xe** lấy bằng cách tách tiêu đề nên có thể sai với tên nhiều từ (vd. "Range Rover").
- Có thể còn tin ảo hoặc nhập sai giá. Các ngoại lai giá cực đoan được loại ở hai đầu 0,5%.

## Làm sạch (`data.py`)
1. Tạo `age` từ `year`.
2. Bỏ tin trùng (`listing_id`) và tin thiếu bất kỳ thuộc tính nào (kể cả km).
3. Loại giá trị vô lý: giá <= 0, km < 0, tuổi < 0, số chỗ <= 0.
4. Loại 0,5% giá thấp nhất và cao nhất.
5. Chuẩn hoá khoảng trắng của các cột chữ.

## Dữ liệu mẫu
`data/sample/sample_cars.csv` là dữ liệu **tổng hợp** sinh bởi `scripts/generate_sample_data.py`, chỉ để chạy thử khi chưa thu thập. Nếu `data/raw/cars.csv` tồn tại, chương trình dùng file đó.
