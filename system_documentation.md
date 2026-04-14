# Tài Liệu Hệ Thống `X-AURUM` (Gold Price Forecasting System)

**X-AURUM** là một hệ thống Trí tuệ Nhân tạo tài chính khép kín, kéo dài từ khâu tự động thu thập mỏ dữ liệu, huấn luyện mô hình Machine Learning, cho đến việc cung cấp dịch vụ Web API có tính năng đồng bộ với thị trường trực tiếp.

Tài liệu này đóng vai trò như một bản thiết kế (Blueprint) mô tả toàn bộ vòng đời của dữ liệu và hệ sinh thái kỹ thuật trong dự án.

---

## 1. Hệ Sinh Thái Công Nghệ (Tech Stack)
Dự án được ứng dụng các công nghệ tiêu chuẩn Enterprise:
- **Ngôn ngữ cốt lõi:** `C#` (.NET 10) / `Python` / `JavaScript` (ES6).
- **Trí tuệ Nhân Tạo:**  `ML.NET v3.0` (Sử dụng thuật toán hồi quy *LightGBM*).
- **Backend Architecture:** `ASP.NET Core Minimal API` kết hợp mô hình bảo vệ `Rate Limiting`.
- **Frontend UI/UX:** `HTML5` + Vanilla CSS `Glassmorphism` UI.
- **Dữ liệu Tích hợp (3rd-Party API):** Binance Public API (Spot Gold Prices), Exchange Rate API (Ngoại hối).
- **Vận hành (DevOps):** `Docker` (Multi-stage build), `GitHub Actions` (CI/CD Deployment).

---

## 2. Kiến Trúc Cấu Trúc Đồ Án (Directory Structure)
Mã nguồn được phân tách minh bạch thành các modules tự do (Decoupled):

```text
d:\Coding Space\Project\Group3\
├── download_data.py            # Auto Scraper kéo giá Vàng từ Binance
├── NEW_GOLD.csv                # Tệp gốc huấn luyện (1000 ngày nến vàng PAXG/USDT)
├── README.md                   # Hướng dẫn tổng quan
├── docker-compose.yml          # Container orchestration script
├── Dockerfile                  # Quy trình đóng hộp hệ thống Web API
|
├── GoldPrice_CLI/              # [MODULE 1] - XƯỞNG AI (ĐÀO TẠO MÔ HÌNH)
│   ├── Program.cs              # Code tải LoadColumn, Train(LightGBM) và Evaluate
│   └── GoldModel.zip           # Não bộ AI sinh ra sau khi huấn luyện (Kết quả)
|
└── GoldPrice_API/              # [MODULE 2] - THỊ TRƯỜNG (DỊCH VỤ CUNG CẤP)
    ├── Program.cs              # Khung xương khởi tạo Server
    ├── GoldModel.zip           # Cùng một cục não AI (được nhúng qua đây)
    ├── Endpoints/
    │   └── PredictionEndpoints.cs # RESTful API Routes (POST manual & GET realtime)
    ├── Extensions/
    │   └── ServiceExtensions.cs   # Nạp Model vào RAM (PredictionEnginePool), chặn Spam
    ├── Models/
    │   └── GoldPriceModels.cs     # Khuôn mẫu Object Data (Open, High, Low, Close, Volume)
    └── wwwroot/
        └── index.html          # Giao diện X-AURUM (Góc nhìn người dùng cuối)
```

---

## 3. Vòng Đời Luân Chuyển Của Dữ Liệu (Workflow)

Trọng tâm sức mạnh của dự án nằm ở sự liền mạch:

### Bước 1: Máy gặt Dữ Liệu (Data Harvesting)
File `download_data.py` gọi lên API của Binance để kéo xuống 1000 ngày lịch sử biến động Giá thật của vàng điện tử (PAXG). Hệ thống tự động ghi lại dữ liệu dưới dạng `NEW_GOLD.csv`. Khác với các dataset bằng tay cổ điển, đây là dữ liệu mang tính ngàn đô phản ảnh chân thực giá Vàng 2026.

### Bước 2: Khởi tạo Trí tuệ nhân tạo (Model Training) 
Chạy `GoldPrice_CLI`. Hệ thống ML.NET đọc `NEW_GOLD.csv`. Nó trích xuất 4 cột: `Open`, `High`, `Low`, `Volume` làm Yếu tố (Features) và dùng cột `Close` làm Mục tiêu học (Label). Thuật toán **LightGBMRegression** sẽ nghiền nát data và nhả ra file lõi: `GoldModel.zip` (Độ chính xác R2 ~0.99).

### Bước 3: Phân Phối Dịch Vụ API (Server Serving)
Gắn não `GoldModel.zip` vào `GoldPrice_API`. Lúc này Server mở cổng trực tuyến `5235` (hoặc `8080` trên máy chủ). 
Đặc biệt, server sử dụng **PredictionEnginePool** để không bao giờ bị nghẽn ngã ba khi có hàng ngàn người truy cập.

### Bước 4: Tự Sống, Tự Phân Tích (Live Automation UI)
Người dùng truy cập vào trang `wwwroot/index.html`.
Ngay lập tức, JavaScript gửi lệnh ngầm tới Server API qua route `/realtime`.
Chính lúc này, **Server sẽ tự động rướn ra ngoài bắn request lấy Tỷ giá Đô-la -> VNĐ và Giá Vàng của giây hiện tại**. AI hấp thu dữ liệu thực và bắn kết quả trở lại màn hình hiển thị dưới dạng Số tiền (VND) trong chớp mắt mà không đợi User phải mỏi tay bấm.

---

## 4. Tài Liệu Thiết Kế RESTful API (API Design)

Nhóm cung cấp 2 Endpoint đáp ứng chuẩn REST cực kỳ quyền lực. Mọi request quá 5 lần/10s sẽ bị khoá với mã lỗi phòng thủ `429 Too Many Requests`.

### `GET /api/v1/predictions/realtime` (Chế độ Bot Tư Động)
- **Công dụng:** Tự lấy giá thị trường Live, tự dự đoán, trả về kết quả mỳ ăn liền.
- **Request Body:** Không có. (Tự server đi lấy data).
- **Response Vàng:**
  ```json
  {
      "success": true,
      "data": {
          "inputsUsed": { "open": 2341.2, "high": 2360.5, "low": 2310.0, "volume": 12500 },
          "predictedClose": 2355.8,
          "predictedCloseVnd": 58895000,
          "liveWorldPrice": 2341.2,
          "exchangeRateVnd": 25000
      }
  }
  ```

### `POST /api/v1/predictions` (Chế độ Nhập tay chuyên nghiệp)
- **Công dụng:** Cho phép các tổ chức/người dùng truyền vào số của riêng họ.
- **Request Body:** (Ngôn ngữ JSON)
  ```json
  {
      "open": 1800,
      "high": 1820,
      "low": 1790,
      "volume": 200500
  }
  ```

---

## 5. Quy Trình Vận Hành Lên Internet (Docker & CI/CD)

Dự án không dừng lại ở Localhost. Hệ thống đã được gói gọi trong hệ tư tưởng vi dịch vụ (Microservice).

- **Kiến trúc Dockerfile Multi-stage:** Trong Dockerfile, code C# sẽ được SDK của .NET biên dịch trên mây. Sau sục sôi, máy chủ sẽ ngắt bỏ phần rác, chỉ giữ lại phần chạy (.dll) nhẹ nhất. Do đó image chỉ ăn vỏn vẹn vài trăm Megabyte bộ nhớ.
- **Github Actions Tự động hóa:** Chỉ cần gõ lệnh đẩy Code lên github (`git push`), một bầy robot ảo của Github sẽ tự chạy, tự đóng tệp `.zip` và tự sinh ra một đường dẫn (GHCR Packages) trên kho đại chúng: `ghcr.io/thanhtrunggdev/group3:latest`.
- Trên bất kỳ VPS (Ubuntu/CentOS), nhóm chỉ cần dán 1 dòng lệnh siêu tốc sau, Web API sẽ vươn mình ra internet thành công 100%:

```bash
sudo docker run -d -p 80:8080 ghcr.io/thanhtrunggdev/group3:latest
```

*(Kết thúc Báo Cáo.)*
