---
marp: true
theme: default
class: lead
backgroundColor: #0d0d0d
color: #f0f0f0
---

# X-AURUM
## Hệ Thống Dự Báo Giá Vàng Theo Thời Gian Thực
Triển khai Web API tích hợp Trí tuệ Nhân tạo & Dữ liệu Thị trường Toàn cầu

**Nhóm 3:** Thành Trung · Xuân Hương · Văn Nguyễn · Quốc Đạt

> 🎙️ **Script (Thành Trung):**
> *"Kính chào thầy cô và các bạn. Nhóm 3 chúng em xin bắt đầu bài báo cáo kết thúc môn với chủ đề: Triển khai Web API tích hợp Mô hình Trí tuệ Nhân tạo và dữ liệu giá Vàng thời gian thực. Hệ thống có tên X-AURUM. Em xin phép đi vào phần đầu tiên."*

---

<!-- SLIDE 1 - Thành Trung -->
## Slide 1: Bài Toán & Kiến Trúc Cốt Lõi
### (Thành Trung)

**Vấn đề đặt ra:**
- Mô hình AI dự báo giá Vàng (ML.NET) chỉ chạy được trên Console nội bộ → Không thể chia sẻ hoặc tái sử dụng từ bên ngoài.
- **Giải pháp:** Bọc thuật toán AI thành **Web Service chuẩn HTTP** bằng **ASP.NET Core Minimal API (.NET 10)**.

**Kiến trúc Clean Architecture:**
```
GoldPrice_API/
├── Endpoints/    → Định tuyến API Routes
├── Models/       → Khuôn mẫu dữ liệu (Input/Output)
└── Extensions/   → Cấu hình DI, Rate Limit, ML Model
```

> 🎙️ **Script:**
> *"Bài toán nhóm em gặp phải là: Mô hình AI chỉ chạy trên máy cục bộ, không ai ngoài nhóm có thể dùng được. Để giải quyết, nhóm em đã bọc toàn bộ logic bên trong một Web API. Framework được chọn là ASP.NET Core Minimal API trên .NET 10 — đây là kiến trúc Microservices tinh gọn nhất hiện nay, loại bỏ hoàn toàn tầng Controller truyền thống thừa thãi. Toàn bộ code được phân tách sạch sẽ thành 3 nhánh: Endpoints định tuyến, Models khai báo dữ liệu, và Extensions quản lý cấu hình."*

---

<!-- SLIDE 2 - Thành Trung -->
## Slide 2: Thiết Kế Hai Luồng Endpoint
### (Thành Trung)

| Endpoint | Method | Mô tả |
|---|---|---|
| `/api/v1/predictions` | `POST` | Client tự nhập dữ liệu OHLCV |
| `/api/v1/predictions/realtime` | `GET` | Bot tự kéo data, không cần input |

**Chuẩn hóa Response RESTful:**
```json
{
  "success": true,
  "data": {
    "predictedClose": 2355.8,
    "predictedCloseVnd": 58895000,
    "liveWorldPrice": 2341.2
  }
}
```

> 🎙️ **Script:**
> *"Nhóm em thiết kế 2 luồng endpoint độc lập. Luồng thứ nhất là POST — dành cho các hệ thống bên ngoài muốn tự truyền vào các chỉ số Open, High, Low, Volume để nhận dự báo. Luồng thứ hai, và đây là điểm đặc biệt: GET /realtime — hoàn toàn không nhận bất kỳ input nào. Chính Server sẽ tự động đi lấy dữ liệu thị trường về và đưa vào mô hình. Mọi Response đều được chuẩn hóa chung một Wrapper JSON có cờ 'success', đảm bảo bất kỳ Client nào cũng parse được an toàn."*

---

<!-- SLIDE 3 - Thành Trung -->
## Slide 3: Tài Liệu API Tự Động Với Swagger (OpenAPI)
### (Thành Trung)

**Tại sao cần Swagger?**
- API đưa ra ngoài mà không có mô tả → Bên thứ 3 không biết cách dùng.
- Swagger tự động đọc code và sinh ra trang tài liệu tương tác đầy đủ.

**Tính năng Swagger trong dự án:**
- ✅ Hiển thị đầy đủ 2 endpoints, mô tả tham số và response schema.
- ✅ Cho phép **Execute** request trực tiếp trên giao diện Web mà không cần Postman.
- ✅ Đây cũng là **công cụ Demo chính** của nhóm trong buổi báo cáo hôm nay.

> 🎙️ **Script:**
> *"Một API chuẩn doanh nghiệp không thể thiếu tài liệu mô tả. Thay vì viết tay file Word hướng dẫn, nhóm em tích hợp Swagger — đây là chuẩn mô tả OpenAPI được cả ngành công nghiệp phần mềm sử dụng. Khi Server khởi động, Swagger tự động đọc code C#, sinh ra một trang web tương tác mô tả toàn bộ endpoints, kiểu dữ liệu vào-ra, và đặc biệt — cho phép người dùng thực thi request ngay trên trang đó mà không cần cài Postman hay bất kỳ công cụ nào. Đây cũng là nơi nhóm em sẽ demo trực tiếp cho thầy cô xem. Em xin nhường phần tiếp theo cho bạn Xuân Hương."*

---

<!-- SLIDE 4 - Xuân Hương -->
## Slide 4: Vấn Đề API Cô Lập & Giải Pháp Tích Hợp
### (Xuân Hương)

**Vấn đề:** Endpoint `/realtime` tự chạy — nhưng lấy dữ liệu thị trường ở đâu?

**Giải pháp:** Server đóng vai **"Client"** gọi ra 2 nguồn API bên ngoài:

| Nguồn API | Mục đích | Dữ liệu lấy về |
|---|---|---|
| **Binance API** | Sàn giao dịch toàn cầu | Giá Vàng PAXG (Open, High, Low, Volume) |
| **Open Exchange Rates API** | Tổ chức tài chính quốc tế | Tỷ giá USD → VND |

> 🎙️ **Script:**
> *"Cảm ơn bạn Trung. Kính thưa thầy cô, bạn Trung vừa giới thiệu endpoint GET /realtime có khả năng tự chạy. Vậy câu hỏi đặt ra là: Server lấy dữ liệu giá vàng ở đâu nếu người dùng không nhập vào? Đây là phần em phụ trách — tích hợp API từ các nguồn bên thứ ba. Nhóm em chọn 2 nguồn: Thứ nhất là Binance — sàn giao dịch tài sản số lớn nhất thế giới, cung cấp API công khai với giá Vàng thực (PAXG) theo từng phiên giao dịch. Thứ hai là Open Exchange Rates — tổ chức cung cấp tỷ giá tiền tệ quốc tế theo thời gian thực, để quy đổi kết quả ra Việt Nam Đồng."*

---

<!-- SLIDE 5 - Xuân Hương -->
## Slide 5: Xử Lý Bất Đồng Bộ & Phân Tích JSON
### (Xuân Hương)

**Luồng xử lý trong `/realtime` Endpoint:**
```
1. Server gửi HTTP GET → Binance API
   └─ Nhận mảng Klines JSON → Trích Open, High, Low, Volume

2. Server gửi HTTP GET → Exchange Rates API
   └─ Đọc node "VND" → Nhận tỷ giá đổi

3. Gộp 4 giá trị → Đưa vào AI Model
   └─ AI trả về PredictedClose (USD)

4. Tính: PredictedClose × VND Rate = Giá VNĐ
   └─ Trả về JSON cho Client
```
Toàn bộ luồng chạy **bất đồng bộ (async/await)** — Server không bị treo khi chờ mạng.

> 🎙️ **Script:**
> *"Đây là luồng xử lý bên trong endpoint /realtime. Khi có yêu cầu gọi vào, Server đồng thời khởi tạo 2 kết nối ra ngoài: một đến Binance để lấy dữ liệu nến vàng, một đến Exchange Rates để lấy tỷ giá. Toàn bộ sử dụng kỹ thuật lập trình bất đồng bộ async/await — nghĩa là Server không bị đứng đợi trong khi chờ phản hồi mạng. Sau khi nhận đủ dữ liệu, hệ thống dùng thư viện System.Text.Json để phân tích cấu trúc JSON phản hồi, trích xuất đúng các node cần thiết mà không cần ánh xạ toàn bộ object — cực kỳ nhẹ và nhanh."*

---

<!-- SLIDE 6 - Xuân Hương -->
## Slide 6: IHttpClientFactory - Giải Pháp Gọi API Chuyên Nghiệp
### (Xuân Hương)

**Vấn đề khi dùng `new HttpClient()` trực tiếp:**
- Mỗi Request tạo ra một kết nối Socket mới → **Cạn kiệt Port (Socket Exhaustion)**.
- Ảnh hưởng nghiêm trọng khi có hàng trăm người dùng cùng lúc.

**Giải pháp: `IHttpClientFactory`**
- Được đăng ký vào **Dependency Injection Container** — quản lý vòng đời bộ gọi HTTP.
- Tái sử dụng kết nối Socket hiệu quả → **Không bao giờ bị cạn kiệt Port**.
- Cấu hình 1 dòng trong `ServiceExtensions.cs`: `builder.Services.AddHttpClient()`

> 🎙️ **Script:**
> *"Một điểm kỹ thuật quan trọng: khi gọi API bên ngoài, nhiều lập trình viên hay viết thẳng 'new HttpClient()'. Cách này tưởng đơn giản nhưng lại gây ra lỗi cực kỳ nguy hiểm gọi là Socket Exhaustion — hệ thống dùng quá nhiều cổng mạng đến mức cạn kiệt, dẫn đến sập Server. Nhóm em giải quyết bằng cách dùng IHttpClientFactory, đăng ký vào hệ thống Dependency Injection của .NET. Factory này quản lý vòng đời của các kết nối HTTP một cách thông minh, tái sử dụng Socket hiệu quả, đảm bảo hệ thống luôn ổn định dù có hàng nghìn người dùng đồng thời. Em xin nhường phần tiếp theo cho bạn Văn Nguyễn."*

---

<!-- SLIDE 7 - Văn Nguyễn -->
## Slide 7: Bài Toán Hiệu Năng - Hosting ML Model
### (Văn Nguyễn)

**Vấn đề đặc thù của Machine Learning API:**
- File `GoldModel.zip` nặng **~43MB**, chứa toàn bộ cấu trúc thần kinh nhân tạo.
- Nếu nạp lại model mỗi lần có Request → **Tốn hàng giây xử lý mỗi lượt gọi**.
- Hệ thống nhiều người dùng đồng thời → **Memory Leak, Server Crash**.

**Yêu cầu giải pháp:**
- Nạp model **đúng 1 lần** lúc khởi động.
- Phục vụ **song song** hàng ngàn request mà không xung đột.

> 🎙️ **Script:**
> *"Kính chào thầy cô, em là Văn Nguyễn, em sẽ trình bày về phần tối ưu hiệu năng và bảo mật hệ thống. Khi tích hợp một mô hình Machine Learning vào Web API, nhóm em gặp phải thách thức đặc thù: file GoldModel.zip nặng 43MB và cực kỳ tốn tài nguyên để khởi tạo. Nếu mỗi lần người dùng gọi API mà Server lại nạp lại file này từ đầu, thì mỗi request sẽ mất nhiều giây và khi nhiều người gọi cùng lúc, Server sẽ hết RAM và sập. Đây là bài toán nhóm em phải giải quyết."*

---

<!-- SLIDE 8 - Văn Nguyễn -->
## Slide 8: PredictionEnginePool - Quản Trị RAM Thông Minh
### (Văn Nguyễn)

**Giải pháp: Object Pooling với `PredictionEnginePool`**

```csharp
// Đăng ký 1 lần duy nhất lúc Server khởi động
builder.Services.AddPredictionEnginePool<ModelInput, ModelOutput>(
    modelName: "GoldModel",
    modelBuilder: ctx => /* Nạp GoldModel.zip vào RAM */
);
```

**Cơ chế hoạt động:**
- 🟢 Server start → Nạp model vào RAM **đúng 1 lần**.
- 🔄 Request đến → **Mượn** Engine từ Pool → Dự báo → **Trả lại** Pool.
- ✅ **Thread-Safe**: Hàng ngàn request chạy song song không xung đột.
- ✅ **Zero Memory Leak**: Pool tự quản lý vòng đời object.

> 🎙️ **Script:**
> *"Giải pháp nhóm em áp dụng là PredictionEnginePool — một kỹ thuật quản lý tài nguyên gọi là Object Pooling. Thay vì tạo mới object mỗi lần dùng, hệ thống tạo sẵn một 'hồ bơi' các Engine đã sẵn sàng trong RAM. Khi có Request đến, Server chỉ việc mượn một Engine từ hồ này, thực hiện dự báo, rồi trả lại. Quá trình này đảm bảo Thread-Safe — nghĩa là hàng nghìn người dùng cùng gọi API một lúc mà không có hai người nào tranh nhau cùng một Engine, không xảy ra xung đột dữ liệu hay Memory Leak."*

---

<!-- SLIDE 9 - Văn Nguyễn -->
## Slide 9: Rate Limiting - Tường Lửa Chống Tấn Công
### (Văn Nguyễn)

**Nguy cơ:** API công khai trên Internet → Dễ bị **DDoS** (tấn công làm nghẽn Server).

**Giải pháp: Fixed Window Rate Limiting (Middleware)**

```
Mỗi IP được cấp phát:
  ┌─────────────────────────────────────┐
  │  Tối đa 5 Request / 10 giây        │
  │  Hàng chờ: 2 Request (Queue)       │
  └─────────────────────────────────────┘

Request thứ 6 trở đi →
  ❌ HTTP 429 Too Many Requests
```

**Điểm mấu chốt:** Middleware chặn ngay ở tầng **HTTP Pipeline** — trước khi Request chạm vào AI Model → Bảo vệ CPU và RAM tuyệt đối.

> 🎙️ **Script:**
> *"Một vấn đề nữa với API công khai là nguy cơ bị tấn công DDoS — kẻ tấn công bắn hàng nghìn Request một giây để làm Server quá tải. Nhóm em tích hợp Rate Limiting Middleware — một lớp bảo vệ nằm ngay ở cổng vào của hệ thống. Cơ chế hoạt động theo thuật toán Fixed Window: mỗi địa chỉ IP chỉ được phép gửi tối đa 5 Request trong 10 giây. Nếu vượt ngưỡng, hệ thống lập tức từ chối bằng HTTP 429 — Too Many Requests. Điều quan trọng là Middleware chặn ở tầng HTTP Pipeline, nghĩa là Request bị trả về ngay từ cổng mà chưa hề chạm vào Model AI — bảo vệ hoàn toàn tài nguyên Server. Phần tiếp theo, mời bạn Quốc Đạt."*

---

<!-- SLIDE 10 - Quốc Đạt -->
## Slide 10: Docker - Đóng Gói & Chuẩn Hóa Môi Trường
### (Quốc Đạt)

**Vấn đề triển khai truyền thống:**
- *"Code chạy trên máy em, sao trên Server lại lỗi?"* → Xung đột môi trường .NET.

**Giải pháp: Docker Containerization**

```dockerfile
# Stage 1: Build (dùng SDK nặng ~800MB)
FROM mcr.microsoft.com/dotnet/sdk:10.0 AS build
RUN dotnet publish -c Release -o /app/publish

# Stage 2: Runtime (chỉ Runtime ~200MB)
FROM mcr.microsoft.com/dotnet/aspnet:10.0 AS final
COPY --from=build /app/publish .
ENTRYPOINT ["dotnet", "GoldPrice_API.dll"]
```

**Multi-stage build** → Image production chỉ **~200MB**, không chứa SDK thừa.

> 🎙️ **Script:**
> *"Kính thưa thầy cô, em là Quốc Đạt, em phụ trách phần triển khai hệ thống lên môi trường thực tế. Khi làm việc theo nhóm, một vấn đề rất phổ biến là: code chạy tốt trên máy của người này nhưng lại lỗi trên máy người khác hoặc trên Server — do xung đột phiên bản .NET. Docker giải quyết triệt để vấn đề này bằng cách đóng gói toàn bộ ứng dụng cùng với môi trường chạy của nó vào một Container cô lập. Nhóm em sử dụng kỹ thuật Multi-stage Build: giai đoạn 1 dùng SDK đầy đủ để biên dịch, giai đoạn 2 chỉ lấy phần runtime tối thiểu. Kết quả là Docker Image chỉ nặng khoảng 200MB — gọn nhẹ và sẵn sàng chạy trên bất kỳ Server nào có Docker."*

---

<!-- SLIDE 11 - Quốc Đạt -->
## Slide 11: CI/CD Pipeline & Triển Khai Trên `nttspace.online`
### (Quốc Đạt)

**Quy trình tự động hóa (GitHub Actions):**
```
git push lên GitHub
    ↓
GitHub Actions tự động kích hoạt
    ↓
Build Docker Image
    ↓
Push lên GitHub Container Registry (GHCR)
    ↓
Server kéo Image mới về & Restart
```

**Nginx Reverse Proxy:**
- Tiếp nhận traffic từ domain `nttspace.online` (Port 80/443).
- Chuyển tiếp vào Docker Container đang lắng nghe nội bộ.
- **Kết quả:** API Live tại `https://nttspace.online/api/v1/predictions`

> 🎙️ **Script:**
> *"Sau khi đã có Docker Image, bước tiếp theo là tự động hóa quy trình deploy. Nhóm em thiết lập GitHub Actions — mỗi khi thành viên push code lên GitHub, một pipeline tự động sẽ chạy: build Docker Image mới, kiểm tra, rồi đẩy lên kho lưu trữ GHCR — GitHub Container Registry. Trên Server thực tế, nhóm em cài Nginx làm Reverse Proxy: Nginx tiếp nhận tất cả request từ domain nttspace.online rồi chuyển tiếp vào container đang chạy bên trong. Nhờ đó, toàn bộ hệ thống X-AURUM hiện đang hoạt động trực tuyến, bất kỳ ai trên thế giới cũng có thể gọi API tại địa chỉ nttspace.online."*

---

<!-- SLIDE 12 - Quốc Đạt - DEMO -->
## Slide 12: Live Demo Trên Swagger
### (Quốc Đạt)

**Demo 1: Endpoint GET /realtime**
1. Mở Swagger UI trên Server.
2. Chọn `GET /api/v1/predictions/realtime` → **Execute**.
3. Server tự gọi Binance + Exchange Rates → AI tính toán → Trả về JSON.
4. Kết quả: `predictedClose ≈ $2350`, `predictedCloseVnd ≈ 120.000.000 VND`.

**Demo 2: Kiểm tra Rate Limiting**
1. Chọn `POST /api/v1/predictions` → Execute liên tiếp **7 lần nhanh**.
2. Lần 1-5: Response `200 OK` bình thường.
3. Lần 6-7: Response `429 Too Many Requests` → ✅ Tường lửa hoạt động.

> 🎙️ **Script:**
> *"Và bây giờ em xin phép demo trực tiếp. Đây là Swagger UI đang chạy trên Server thật tại nttspace.online. Em sẽ gọi GET /realtime — thầy cô thấy Server tự động kéo giá vàng thực tế từ Binance, gộp với tỷ giá từ Exchange Rates, đưa vào mô hình AI và trả về kết quả là hơn 120 triệu đồng cho mỗi đơn vị giao dịch. Tiếp theo, em sẽ giả lập tấn công spam bằng cách bấm Execute liên tục — thầy cô thấy từ lần thứ 6 trở đi hệ thống lập tức trả về HTTP 429, tường lửa Rate Limiting hoạt động hoàn hảo. Đó là toàn bộ hệ thống X-AURUM của Nhóm 3. Nhóm em xin cảm ơn thầy cô và xin lắng nghe câu hỏi phản biện ạ."*

---

# Cảm Ơn Thầy Cô & Hội Đồng!

**Nhóm 3** xin lắng nghe câu hỏi và phản biện.

| Thành viên | Phần trình bày |
|---|---|
| Thành Trung | Kiến trúc API & Swagger |
| Xuân Hương | Tích hợp 3rd-Party APIs |
| Văn Nguyễn | Hiệu năng & Bảo mật |
| Quốc Đạt | DevOps & Live Demo |

**`nttspace.online`** — Hệ thống đang chạy Live!
