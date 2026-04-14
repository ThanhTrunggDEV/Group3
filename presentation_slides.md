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

**Nhóm 3:** Xuân Hương · Quốc Đạt · Văn Nguyễn · Thành Trung

> 🎙️ **Script (Xuân Hương):**
> *"Kính chào thầy cô và các bạn. Nhóm 3 chúng em xin bắt đầu bài báo cáo kết thúc môn với chủ đề: Triển khai Web API tích hợp Mô hình Trí tuệ Nhân tạo và dữ liệu giá Vàng thời gian thực. Hệ thống có tên X-AURUM. Em là Xuân Hương, em xin phép đi vào phần đầu tiên."*

---

<!-- SLIDE 1 - Xuân Hương -->
## Slide 1: Bài Toán & Kiến Trúc Cốt Lõi
### (Xuân Hương)

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
> *"Bài toán đầu tiên nhóm em gặp phải là: Mô hình AI chỉ chạy trên máy cục bộ, không ai ngoài nhóm có thể dùng được. Để giải quyết, chúng em đã bọc toàn bộ logic này bên trong một Web API. Framework được chọn là ASP.NET Core Minimal API trên .NET 10 — đây là kiến trúc Microservices tinh gọn nhất hiện nay, loại bỏ hoàn toàn tầng Controller truyền thống phức tạp. Toàn bộ code được phân tách sạch sẽ thành 3 nhánh: Endpoints định tuyến, Models khai báo dữ liệu, và Extensions quản lý cấu hình."*

---

<!-- SLIDE 2 - Xuân Hương -->
## Slide 2: Thiết Kế Hai Luồng Endpoint
### (Xuân Hương)

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
    "predictedCloseVnd": 120000000,
    "liveWorldPrice": 2341.2
  }
}
```

> 🎙️ **Script:**
> *"Nhóm em thiết kế 2 luồng endpoint độc lập. Luồng thứ nhất là POST — dành cho các hệ thống bên ngoài muốn tự truyền vào các chỉ số Open, High, Low, Volume để nhận dự báo. Luồng thứ hai, và đây là điểm đặc biệt: GET /realtime — hoàn toàn không nhận bất kỳ input nào. Chính Server sẽ tự động đi lấy dữ liệu thị trường về và đưa vào mô hình. Mọi Response đều được chuẩn hóa chung một Wrapper JSON có cờ 'success', đảm bảo hệ thống gọi đến parse dữ liệu dễ dàng và an toàn."*

---

<!-- SLIDE 3 - Xuân Hương -->
## Slide 3: Tài Liệu API Tự Động Với Swagger (OpenAPI)
### (Xuân Hương)

**Tại sao cần Swagger?**
- API đưa ra ngoài mà không có mô tả → Bên thứ 3 không biết cách dùng.
- Swagger tự động đọc code và sinh ra trang tài liệu tương tác đầy đủ.

**Tính năng Swagger trong dự án:**
- ✅ Hiển thị đầy đủ 2 endpoints, mô tả tham số và response schema.
- ✅ Cho phép **Execute** request trực tiếp trên giao diện Web mà không cần Postman.
- ✅ Đây cũng là **công cụ Demo chính** của nhóm trong buổi báo cáo hôm nay.

> 🎙️ **Script:**
> *"Hơn nữa, một API chuẩn doanh nghiệp không thể thiếu tài liệu mô tả. Thay vì viết tay file hướng dẫn, nhóm em tích hợp luôn Swagger — chuẩn mô tả OpenAPI tiên tiến nhất. Khi Server hoạt động, Swagger sẽ tự sinh trang web mô tả toàn bộ endpoints, kiểu dữ liệu vào-ra, và còn cho phép người dùng chạy thử (Execute) ngay trên web mà không cần cài thêm công cụ như Postman. Lát nữa nhóm em cũng sẽ dùng Swagger để demo. Em xin kết thúc phần kiến trúc, tiếp theo mời bạn Quốc Đạt."*

---

<!-- SLIDE 4 - Quốc Đạt -->
## Slide 4: Tích Hợp API Bên Thứ 3 (Binance & ExchangeRate)
### (Quốc Đạt)

**Bài thi 3: Sử dụng API từ nguồn bên ngoài (3rd-Party APIs)**

**Nguồn 1: Binance Public API**
- Mục đích: Lấy giá Vàng Spot theo phiên giao dịch.
- Method & URL: `GET api.binance.com/api/v3/klines`
- Dữ liệu: Open, High, Low, Volume từ mảng Klines JSON.

**Nguồn 2: Open Exchange Rates API**
- Mục đích: Lấy tỷ giá USD → VND hiện tại.
- Method & URL: `GET open.er-api.com/v6/latest/USD`
- Dữ liệu: rates.VND

> 🎙️ **Script:**
> *"Cảm ơn bạn Hương. Kính thưa thầy cô, em là Quốc Đạt, em xin trình bày về phần tích hợp 3rd-Party APIs. Quay lại bài toán: Server lấy dữ liệu giá vàng ở đâu nếu người dùng không nhập vào? Nhóm em để Server đóng vai Client đi gọi ra ngoài. Nhóm tự động truy xuất từ 2 nguồn thực tế: Binance để lấy giá nến Vàng PAXG theo ngày, và Open Exchange Rates để lấy tỷ giá USD sang VND thời gian thực. Sau đó lấy kết quả AI nhân với tỷ giá để ra được số tiền VNĐ hiện tại."*

---

<!-- SLIDE 5 - Quốc Đạt -->
## Slide 5: Xử Lý Bất Đồng Bộ & Phân Tích JSON
### (Quốc Đạt)

**Luồng xử lý trong `/realtime` Endpoint:**
```
1. Server gửi HTTP GET → Binance API
2. Server gửi HTTP GET → Exchange Rates API
3. Gộp 4 giá trị → Model AI tính toán
4. Kết quả x Tỷ giá → Trả về JSON cho Client
```

**Tại sao dùng async/await?**
- Server không bị 'đứng' khi chờ mạng.
- Xử lý nhiều request đồng thời, tăng tổng throughput.
- Phân tích Node JSON trực tiếp (DOM Tree) không cần map toàn bộ object.

> 🎙️ **Script:**
> *"Để luồng gọi này hiệu quả nhất, nhóm em sử dụng kỹ thuật lập trình bất đồng bộ async/await. Khi có yêu cầu, Server đồng thời khởi tạo 2 kết nối ra Binance và Exchange Rates. Khi đó luồng xử lý không hề bị chặn lại chờ đợi mạng, giúp Server tiết kiệm tài nguyên. Sau khi nhận đủ dữ liệu, hệ thống dùng System.Text.Json đọc trực tiếp các Node cần thiết trên chuỗi JSON gửi về mà không cần ánh xạ (map) ra toàn bộ Object lớn, rất nhẹ và tiết kiệm thanh ghi."*

---

<!-- SLIDE 6 - Quốc Đạt -->
## Slide 6: IHttpClientFactory - Gọi API Chuyên Nghiệp
### (Quốc Đạt)

**Vấn đề với `new HttpClient()`:**
- Cạn kiệt Port (Socket Exhaustion) nếu người dùng gọi liên tục.

**Giải pháp: IHttpClientFactory**
- Quản lý tập trung tại Dependency Injection Container.
- Tái sử dụng kết nối Socket.
- `builder.Services.AddHttpClient();`

> 🎙️ **Script:**
> *"Một điểm mạnh nữa về kỹ thuật: nhóm em không khởi tạo 'new HttpClient' mỗi khi gọi ra ngoài, làm như vậy sẽ dẫn đến Socket Exhaustion — hiểu nôm na là cạn kiệt cổng mạng khi scale lớn. Chúng em dùng IHttpClientFactory, cung cấp sẵn bởi .NET DI Container. Factory này tái sử dụng các kết nối HTTP vô cùng thông minh, không lo rò rỉ Socket và giúp ứng dụng chịu tải cao cực tốt. Phần tiếp theo về hiệu năng, xin mời bạn Văn Nguyễn."*

---

<!-- SLIDE 7 - Văn Nguyễn -->
## Slide 7: Bài Toán Hiệu Năng - Hosting ML Model
### (Văn Nguyễn)

**Vấn đề đặc thù khi Host Machine Learning làm REST API:**
- File `GoldModel.zip` nặng **~43MB**.
- Nếu nạp lại model mỗi lần có Request → Tốn hàng giây xử lý, rất chậm.

**Kịch bản nguy hiểm:** Nạp lại model mỗi request = Tràn RAM (Memory Leak)

```csharp
// SAI -- nạp lại model mỗi request
app.MapPost("/predict", (input) => {
    var ctx = new MLContext();
    var model = ctx.Model.Load("GoldModel.zip", ...);
    // -> RAM tăng vô hạn theo số lượng request
});
```

> 🎙️ **Script:**
> *"Kính chào thầy cô, em là Văn Nguyễn, em phụ trách tối ưu hiệu năng và bảo mật hệ thống. File AI học máy của nhóm nặng hơn 40MB. Thách thức lớn là: nếu mỗi lúc nhận Request, API lại đọc file 40MB này từ đĩa vào RAM thì sẽ mất hàng chục giây cho mỗi lượt tương tác, vài nghìn Request vào cùng lúc chắc chắn Server sẽ sập vì tràn RAM. Đoạn code sai lầm ở trên là thứ chúng em đã loại bỏ hoàn toàn."*

---

<!-- SLIDE 8 - Văn Nguyễn -->
## Slide 8: PredictionEnginePool - Quản Trị RAM
### (Văn Nguyễn)

**Giải pháp: PredictionEnginePool (Object Pooling)**

```csharp
// ĐÚNG -- đăng ký 1 lần duy nhất lúc Server khởi động
builder.Services.AddPredictionEnginePool<ModelInput, ModelOutput>(
    modelName: "GoldModel",
    modelBuilder: ctx => ctx.Model.Load("GoldModel.zip", ...)
);
```

**Cơ chế hoạt động:**
- Server start → Nạp model vào RAM **đúng 1 lần**.
- Tái sử dụng: Mượn Engine → Dự báo → Trả lại Pool.
- **Thread-safe**: Không xung đột, không rò rỉ Memory Leak.

> 🎙️ **Script:**
> *"Cách chúng em giải quyết là nhúng PredictionEnginePool — một dạng Object Pooling của thư viện Microsoft.ML. Thay vì load model liên tục, Pooling chỉ load model lên RAM đúng 1 lần duy nhất khi Server khởi động. Khi có Request, API chỉ mượn một Engine đang rảnh trong hồ bơi (Pool), dùng xong lại trả về. Cơ chế này an toàn về Thread (Thread-Safe) cho dù có hàng nghìn lượt Request đồng thời và loại bỏ hoàn toàn hiện tượng Memory Leak."*

---

<!-- SLIDE 9 - Văn Nguyễn -->
## Slide 9: Rate Limiting - Tường Lửa Chống Tấn Công
### (Văn Nguyễn)

**Cấu hình Fixed Window Rate Limiting Middleware:**
- **Permit Limit:** 5 Request
- **Window:** 10 giây / IP
- **Kết quả khi vượt quá:** HTTP 429 Too Many Requests

**Hệ quả bảo vệ:**
- Bị chặn tức thì tại tầng HTTP Pipeline.
- Chưa chạm vào AI Model → CPU & RAM hoàn toàn an toàn.

> 🎙️ **Script:**
> *"Bên cạnh tối ưu RAM, API của chúng em là công khai nên rất dễ bị phá hoại hoặc spam bằng DDoS. Nhóm em đã bật tường lửa Rate Limiting theo thuật toán Fixed Window. Mỗi IP sẽ chỉ được gọi 5 Request trong 10 giây. Hãy tưởng tượng có bot spam 1 triệu Request, nó sẽ bị chặn ngay tại tầng mạng HTTP Pipeline và trả về HTTP 429 Too Many Requests, hoàn toàn không đẩy lượng rác đó vào phân tích AI. Server được bảo vệ tuyệt đối. Tiếp theo mời bạn Thành Trung."*

---

<!-- SLIDE 10 - Thành Trung -->
## Slide 10: Docker - Đóng Gói & Chuẩn Hóa Môi Trường
### (Thành Trung)

**Vấn đề:** Môi trường khác nhau sinh lỗi (Code chạy máy em, sao lên Server lỗi?).

**Giải pháp: Docker Multi-stage Build**

```dockerfile
# Stage 1: Build (SDK ~800MB)
FROM mcr.microsoft.com/dotnet/sdk:10.0 AS build
...
# Stage 2: Runtime (Chỉ Runtime ~200MB)
FROM mcr.microsoft.com/dotnet/aspnet:10.0 AS final
COPY --from=build /app/publish .
```

Hình ảnh triển khai cuối chỉ ~200MB, đóng gói chặt chẽ chỉ 1 lệnh `docker-compose up -d`.

> 🎙️ **Script:**
> *"Cảm ơn bạn Nguyễn. Thưa thầy cô, em là Thành Trung, em xin khép lại với kiến trúc triển khai DevOps. Lúc làm nhóm, một vấn đề cực kỳ khó chịu là 'Code máy em chạy nhưng copy sang máy bạn cài .NET bản khác là lỗi'. Chúng em chấm dứt điều này với Docker. Chúng em đóng thùng toàn bộ Server vào Container, viết Dockerfile theo Multi-Stage Build — giai đoạn một dùng SDK cả Gb để Build, giai đoạn hai chuyển thành Runtime nhẹ tựa lông hồng, chỉ 200MB. Mọi máy chạy đều đồng nhất bản chất, 1 lệnh duy nhất là hệ thống vận hành."*

---

<!-- SLIDE 11 - Thành Trung -->
## Slide 11: CI/CD & Triển Khai Trên nttspace.online
### (Thành Trung)

**Quy trình tự động hóa (GitHub Actions):**
1. [PUSH] git push lên GitHub
2. >> GitHub Actions kích hoạt
3. >> Build Docker Image
4. >> Push lên GHCR (GitHub Container Registry)
5. >> Server tự pull image mới & restart.

**Nginx Reverse Proxy:** Traffic HTTPS (Cổng 443) đi vào `nttspace.online` → Proxy an toàn chuyển vào Docker (Cổng 5235).

> 🎙️ **Script:**
> *"Để tiết kiệm công sức deploy, nhóm tích hợp Workflow GitHub Actions. Mỗi khi ấn Push Code vòng tuần hoàn sẽ chạy: Git Server tự Build Docker Image, đẩy về Registry, và Virtual Machine trên Cloud sẽ tự biết kéo Image mới về khởi động lại không gián đoạn dịch vụ. Ngay hiện tại, hệ thống đã được Public Production tại domain nttspace.online với chứng chỉ bảo mật đầy đủ, sử dụng Nginx Reverse Proxy làm mặt tiền hứng toàn bộ traffic để truyền vào bên trong."*

---

<!-- SLIDE 12 - Thành Trung -->
## Slide 12: Live Demo Trên Swagger
### (Thành Trung)

**Demo 1: GET /api/v1/predictions/realtime**
1. Mở Swagger UI trên `nttspace.online`.
2. Trả JSON giá thế giới + giá chuyển đổi VND.

**Demo 2: Rate Limiting**
1. Thực thi `POST` liên tục trên Swagger
2. Vượt hạn mức → báo lỗi hệ thống cảnh báo đỏ 429.

> 🎙️ **Script:**
> *"Và sau đây, không có gì thuyết phục hơn là chạy demo thực tế. Trên bảng lớn là màn hình Swagger thật từ tên miền chính thức của nhóm. Em sẽ thực thi lệnh GET Realtime không cấp dữ liệu — màn hình tức thời hiển thị giá vàng thế giới và đổi ra VND trực tiếp. Kế đến, em xin spam nút Execute liên tục vào Endpoint POST. Như bạn Nguyễn đã thiết kế phần trước, thầy cô có thể thấy màn hình bật qua trạng thái 429 Too Many Requests — tường lửa đã thành công khóa IP của chính em lại. Đó là tất cả tính năng của dự án X-AURUM!"*

---

# CẢM ƠN THẦY CÔ & HỘI ĐỒNG!
Nhóm 3 xin lắng nghe câu hỏi phản biện.

| Thành viên | Phần trình bày |
|---|---|
| Xuân Hương | Kiến trúc API & Swagger |
| Quốc Đạt | Tích hợp 3rd-Party APIs |
| Văn Nguyễn | Hiệu năng & Bảo mật |
| Thành Trung | DevOps & Live Demo |

**`nttspace.online`**
