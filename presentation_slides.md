---
marp: true
theme: default
class: lead
backgroundColor: #1a1a1a
color: #ffffff
---

# X-AURUM: THE GOLD PRICE API 
Triển khai Mô hình Trí Tuệ Nhân Tạo thành Giao thức Web API
**Nhóm 3:** Thành Trung - Văn Nguyễn - Xuân Hương - Quốc Đạt

---

<!-- Speaker: Thành Trung -->
## VẤN ĐỀ VÀ MỤC TIÊU DỰ ÁN 🎯

- **Thực trạng:** 
  - Mô hình AI dự đoán giá Vàng (`GoldModel.zip`) hoạt động xuất sắc.
  - Tuy nhiên, file tĩnh chỉ chạy được trên dòng lệnh Local (Console), khó tiếp cận.
- **Giải pháp - "Vượt rào cản nền tảng":** 
  - Xây dựng một **Web API (RESTful)** bọc lấy lõi AI.
  - Cho phép người dùng hoặc hệ thống khác gửi data lên qua giao thức `HTTP POST`.
  - Kết quả trả về JSON chuẩn hóa.

---

<!-- Speaker: Thành Trung -->

## KIẾN TRÚC MINIMAL API CỐT LÕI ⚙️

- Sử dụng **ASP.NET Core 10 Minimal API**: Kiến trúc tinh gọn, hiệu năng cao nhất hiện nay dành cho microservices.
- **PredictionEnginePool**: Khác với việc nạp file truyền thống tốn dung lượng, dự án sử dụng EnginePool để:
  - Nạp mô hình AI vào RAM đúng 1 lần.
  - Chia sẻ tài nguyên (Thread-safe) an toàn.
  - Phục vụ song song hàng nghìn Request mà không sợ crash Server.

---

<!-- Speaker: Văn Nguyễn -->
## CLEAN ARCHITECTURE 🏗️

Thay vì code toàn bộ logic vào nội tại 1 file `Program.cs`, hệ thống được tách lớp chuẩn doanh nghiệp:

1. **Thư mục Models (`GoldPriceModels.cs`):** 
   Nơi khai báo khắt khe định dạng Input (OHLC) và Output (PredictedClose).
2. **Thư mục Endpoints (`PredictionEndpoints.cs`):** 
   Tách biệt Router định tuyến API (`POST /api/v1/predictions`).
3. **Thư mục Extensions (`ServiceExtensions.cs`):** 
   Gói gọn các cấu hình Dependency Injection phức tạp (Nạp mô hình, Rate Limit,...).

---

<!-- Speaker: Văn Nguyễn -->
## RÀO CHẮN BẢO VỆ CHỐNG SPAM/DDOS 🛡️

*Bất cứ API đại chúng (Public) nào mở ra ngoài cũng đối diện nguy cơ bị tấn công DDoS.*

- Công cụ: Tích hợp **Rate Limiter (Fixed Window)** của ASP.NET.
- Cấu hình thực tế dự án:
  - **Giới hạn (Permit Limit):** Tối đa 5 yêu cầu phân tích giá vàng...
  - **Chu kỳ (Window):** ...trong vòng mỗi 10 giây cho từng người dùng.
  - **Hàng chờ (Queue):** Cho phép 2 yêu cầu xếp hàng nợ.
- Nếu cố tình spam: Hệ thống kích hoạt phòng vệ và trả về cờ **HTTP 429: Too Many Requests.**

---

<!-- Speaker: Xuân Hương -->
## GIAO DIỆN CLIENT X-AURUM 💻

Làm thế nào để người dùng giao tiếp với API mượt mà nhất?
- Giao diện **Dark Mode Glassmorphism**: Không gian thiết kế kính mờ trong suốt, viễn tưởng.
- Thành phần: 
  - Input kỹ thuật như Terminal cổ điển.
  - Khối Lõi Vàng hiển thị dự đoán trung tâm.
- Công nghệ: CSS + Animation động.

---

<!-- Speaker: Xuân Hương -->
## KẾT NỐI API BẰNG GIAO TÍCH BẤT ĐỒNG BỘ ⚡

Trang Frontend kết nối với API Backend dưới dạng Serverless.
- Dùng `Fetch API` thực thi gửi lệnh ngầm HTTP POST.
- Bắt và xử lý ngoại lệ vòng kín:
  - Báo giá trị chạy số thực (nếu API OK).
  - Tự động bắt cảnh báo nếu Server bắn lỗi `429` Rate Limit và hiện "Cảnh báo phòng vệ" đỏ góc màn hình.

---

<!-- Speaker: Quốc Đạt -->
## TRIỂN KHAI MÁY CHỦ BẰNG DOCKER 🐳

API hoạt động nội bộ không có ý nghĩa nếu không thể mang lên Server.
- Hệ thống được chứa hóa (**Containerization**).
- Tích hợp **Dockerfile** sử dụng Multi-stage build (vừa biên dịch vừa đóng gói cực kỳ gọn nhẹ).
- Kết hợp **Docker-Compose**: Cho phép khởi động toàn bộ cụm Server Web API kèm cấu hình Mạng chỉ với 1 lệnh `docker compose up` trên mọi hệ điều hành Linux/Windows.

---

<!-- Speaker: Quốc Đạt -->
## TỰ ĐỘNG HÓA CI/CD ĐẠT CHUẨN DEVOPS ♾️

Loại bỏ thao tác Deploy bằng tay cực khổ:
- Viết sẵn hệ thống kịch bản **GitHub Actions**.
- Quy trình: Bất kì thành viên nào push thay đổi Code (C# / HTML) lên nhánh chính `main`.
- Robot sẽ tự động dò tìm lỗi `> Build ảnh Docker Server > Đẩy ảnh nén đó lên kho Github Container Registry (GHCR)`.
- Sẵn sàng dùng cho mọi Server VPS ảo trên thế giới tải xuống ngay tắp lự.

---

# BÙNG NỔ VÀ TRÌNH DIỄN (LIVE DEMO) 🚀
*Mời thầy cô cùng nhìn ngắm Server hoạt động thực tế!*

1. **Bước 1:** Trình bày UI giao diện, nhập 4 chỉ số OHLC thực tế lấy từ dữ liệu vàng 2026. Bấm Execute.
2. **Bước 2:** Mô hình chớp sáng, trả về giá đóng cửa (Close Price) với độ tin cậy 98%.
3. **Bước 3:** Cố ý bấm Execute 7 lần liên tiếp trong 3 giây -> Màn hình văng ngay cảnh báo Đỏ: "Defensive Measures Engaged - Rate Limit Exceeded".

---

# CÁM ƠN THẦY CÔ VÀ HỘI ĐỒNG XÉT DUYỆT!
*Nhóm 3 xin lắng nghe các câu hỏi hoặc phản biện từ quý thầy cô.*
