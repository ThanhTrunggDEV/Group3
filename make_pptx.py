from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt
import copy

# ────────── PALETTE ──────────
BG_DARK     = RGBColor(0x0D, 0x0D, 0x0D)
GOLD        = RGBColor(0xF5, 0xC5, 0x18)
WHITE       = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT_GRAY  = RGBColor(0xCC, 0xCC, 0xCC)
DARK_GRAY   = RGBColor(0x33, 0x33, 0x33)
ACCENT_BLUE = RGBColor(0x3B, 0x82, 0xF6)

W = Inches(13.33)
H = Inches(7.5)

prs = Presentation()
prs.slide_width  = W
prs.slide_height = H

BLANK = prs.slide_layouts[6]  # completely blank

# ────────── HELPERS ──────────
def set_bg(slide, color=BG_DARK):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = color

def add_rect(slide, l, t, w, h, color):
    shape = slide.shapes.add_shape(1, l, t, w, h)
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    return shape

def add_textbox(slide, text, l, t, w, h,
                font_size=18, bold=False, color=WHITE,
                align=PP_ALIGN.LEFT, italic=False, wrap=True):
    txBox = slide.shapes.add_textbox(l, t, w, h)
    txBox.word_wrap = wrap
    tf = txBox.text_frame
    tf.word_wrap = wrap
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(font_size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    return txBox

def add_label(slide, text, l, t, w, h, color=GOLD):
    """Small pill/label box"""
    box = add_rect(slide, l, t, w, h, color)
    tf = slide.shapes[-1].text_frame if False else None
    tb = add_textbox(slide, text, l, t, w, h,
                     font_size=11, bold=True, color=BG_DARK, align=PP_ALIGN.CENTER)
    return tb

def gold_line(slide, t):
    """Full-width gold separator line"""
    add_rect(slide, Inches(0), t, W, Inches(0.04), GOLD)

def add_bullet_block(slide, items, l, t, w, font_size=15, color=LIGHT_GRAY):
    """Add a list of bullet items stacked vertically"""
    line_h = Inches(0.4)
    for item in items:
        prefix = "  •  " if not item.startswith("    ") else "      ▸  "
        text = prefix + item.strip()
        add_textbox(slide, text, l, t, w, line_h,
                    font_size=font_size, color=color)
        t += line_h
    return t

def add_code_block(slide, code, l, t, w):
    """Dark code box"""
    lines = code.strip().split("\n")
    h = Inches(0.3) * len(lines) + Inches(0.2)
    add_rect(slide, l, t, w, h, DARK_GRAY)
    add_textbox(slide, code.strip(), l + Inches(0.1), t + Inches(0.08),
                w - Inches(0.2), h, font_size=11, color=GOLD)
    return t + h

# ════════════════════════════════════════════════════
# SLIDE 0 — TITLE
# ════════════════════════════════════════════════════
def make_title_slide():
    slide = prs.slides.add_slide(BLANK)
    set_bg(slide)
    # Gold top bar
    add_rect(slide, 0, 0, W, Inches(0.12), GOLD)
    # Gold bottom bar
    add_rect(slide, 0, H - Inches(0.12), W, Inches(0.12), GOLD)

    # Main title
    add_textbox(slide, "X-AURUM",
                Inches(1), Inches(1.2), Inches(11), Inches(1.4),
                font_size=72, bold=True, color=GOLD, align=PP_ALIGN.CENTER)

    add_textbox(slide, "Hệ Thống Dự Báo Giá Vàng Theo Thời Gian Thực",
                Inches(1), Inches(2.7), Inches(11), Inches(0.8),
                font_size=24, color=WHITE, align=PP_ALIGN.CENTER)

    add_textbox(slide, "Triển khai Web API tích hợp Trí tuệ Nhân tạo & Dữ liệu Thị trường Toàn cầu",
                Inches(1), Inches(3.3), Inches(11), Inches(0.7),
                font_size=16, color=LIGHT_GRAY, align=PP_ALIGN.CENTER, italic=True)

    gold_line(slide, Inches(4.2))

    add_textbox(slide, "Nhóm 3  ·  Thành Trung  ·  Xuân Hương  ·  Văn Nguyễn  ·  Quốc Đạt",
                Inches(1), Inches(4.4), Inches(11), Inches(0.6),
                font_size=16, color=LIGHT_GRAY, align=PP_ALIGN.CENTER)

    add_textbox(slide, "nttspace.online", Inches(1), Inches(5.1), Inches(11), Inches(0.5),
                font_size=14, color=GOLD, align=PP_ALIGN.CENTER, italic=True)

make_title_slide()

# ════════════════════════════════════════════════════
# SLIDES 1-3 — Thành Trung
# ════════════════════════════════════════════════════

def make_content_slide(title, speaker, content_fn):
    slide = prs.slides.add_slide(BLANK)
    set_bg(slide)
    add_rect(slide, 0, 0, W, Inches(0.08), GOLD)
    # Speaker label
    add_rect(slide, Inches(0), Inches(0.08), Inches(2.8), Inches(0.45), RGBColor(0x1E,0x1E,0x1E))
    add_textbox(slide, f"🎙  {speaker}", Inches(0.1), Inches(0.08), Inches(2.6), Inches(0.45),
                font_size=11, color=GOLD)
    # Title
    add_textbox(slide, title, Inches(0.5), Inches(0.65), Inches(12.3), Inches(0.75),
                font_size=28, bold=True, color=WHITE)
    gold_line(slide, Inches(1.45))
    content_fn(slide)
    return slide

# ── Slide 1
def s1(slide):
    add_textbox(slide, "Vấn đề đặt ra", Inches(0.5), Inches(1.6), Inches(6), Inches(0.4),
                font_size=15, bold=True, color=GOLD)
    add_bullet_block(slide, [
        "Mô hình AI (ML.NET) chỉ chạy được trên Console nội bộ.",
        "Không thể chia sẻ hoặc tái sử dụng từ các hệ thống khác."
    ], Inches(0.5), Inches(2.05), Inches(5.8))

    add_textbox(slide, "Giải pháp: ASP.NET Core Minimal API (.NET 10)", Inches(0.5), Inches(2.95), Inches(6), Inches(0.4),
                font_size=15, bold=True, color=GOLD)
    add_bullet_block(slide, [
        "Bọc thuật toán AI thành Web Service chuẩn HTTP.",
        "Loại bỏ Controllers truyền thống — kiến trúc Microservices tinh gọn nhất.",
    ], Inches(0.5), Inches(3.4), Inches(5.8))

    add_textbox(slide, "Clean Architecture", Inches(7), Inches(1.6), Inches(5.8), Inches(0.4),
                font_size=15, bold=True, color=GOLD)
    add_code_block(slide,
        "GoldPrice_API/\n├── Endpoints/    → Định tuyến API Routes\n├── Models/       → Input/Output Schema\n└── Extensions/   → DI, Rate Limit, ML Model",
        Inches(7), Inches(2.1), Inches(5.8))

make_content_slide("Slide 1 · Bài Toán & Kiến Trúc Cốt Lõi", "Thành Trung", s1)

# ── Slide 2
def s2(slide):
    # Table header
    cols = [Inches(0.5), Inches(3.5), Inches(7.5)]
    headers = ["Endpoint", "Method", "Mô tả"]
    col_w   = [Inches(3), Inches(1.5), Inches(5)]
    for i,(x,hdr) in enumerate(zip(cols, headers)):
        add_rect(slide, x, Inches(1.6), col_w[i], Inches(0.4), GOLD)
        add_textbox(slide, hdr, x+Inches(0.05), Inches(1.6), col_w[i], Inches(0.4),
                    font_size=13, bold=True, color=BG_DARK)
    rows = [
        ["/api/v1/predictions", "POST", "Client tự nhập dữ liệu OHLCV"],
        ["/api/v1/predictions/realtime", "GET", "Bot tự kéo data — không cần input"],
    ]
    for r, row in enumerate(rows):
        bg = RGBColor(0x19,0x19,0x19) if r%2==0 else RGBColor(0x22,0x22,0x22)
        for i,(x,cell) in enumerate(zip(cols, row)):
            add_rect(slide, x, Inches(2.0+r*0.45), col_w[i], Inches(0.45), bg)
            clr = GOLD if i==1 else LIGHT_GRAY
            add_textbox(slide, cell, x+Inches(0.05), Inches(2.0+r*0.45), col_w[i], Inches(0.45),
                        font_size=12, color=clr)

    add_textbox(slide, "Chuẩn hóa Response RESTful (JSON Wrapper)", Inches(0.5), Inches(3.15), Inches(6), Inches(0.4),
                font_size=15, bold=True, color=GOLD)
    add_code_block(slide,
        '{\n  "success": true,\n  "data": {\n    "predictedClose": 2355.8,\n    "predictedCloseVnd": 58895000,\n    "liveWorldPrice": 2341.2\n  }\n}',
        Inches(0.5), Inches(3.6), Inches(6))

    add_textbox(slide, "✅  Mọi Client đều parse an toàn\n✅  Dễ mở rộng thêm trường mới\n✅  Phân biệt rõ luồng Manual vs Auto",
                Inches(7), Inches(3.15), Inches(5.8), Inches(2),
                font_size=14, color=LIGHT_GRAY)

make_content_slide("Slide 2 · Thiết Kế Hai Luồng Endpoint", "Thành Trung", s2)

# ── Slide 3
def s3(slide):
    add_textbox(slide, "Tại sao cần Swagger / OpenAPI?", Inches(0.5), Inches(1.6), Inches(12), Inches(0.4),
                font_size=15, bold=True, color=GOLD)
    add_bullet_block(slide, [
        "API đưa ra ngoài mà không có mô tả → Bên thứ 3 không biết cách dùng.",
        "OpenAPI là chuẩn mô tả API được cả ngành công nghiệp sử dụng.",
        "Swagger UI tự động đọc code C# → Sinh trang tài liệu tương tác đầy đủ.",
    ], Inches(0.5), Inches(2.1), Inches(12))

    add_textbox(slide, "Tính năng đã tích hợp", Inches(0.5), Inches(3.3), Inches(12), Inches(0.4),
                font_size=15, bold=True, color=GOLD)
    items = [
        "✅  Hiển thị đầy đủ 2 endpoints, mô tả tham số và response schema.",
        "✅  Cho phép Execute request ngay trên giao diện Web — không cần Postman.",
        "✅  Là công cụ Demo trực tiếp trong buổi báo cáo hôm nay.",
    ]
    add_bullet_block(slide, items, Inches(0.5), Inches(3.75), Inches(12))

    add_rect(slide, Inches(0.5), Inches(5.4), Inches(12.3), Inches(0.75), RGBColor(0x1B,0x2A,0x1B))
    add_textbox(slide, "💡  Swagger chính là cổng giao tiếp giữa nhóm và thế giới bên ngoài.",
                Inches(0.7), Inches(5.45), Inches(12), Inches(0.65),
                font_size=14, color=RGBColor(0x86,0xEF,0xAC), italic=True)

make_content_slide("Slide 3 · Tài Liệu API Tự Động Với Swagger", "Thành Trung", s3)

# ════════════════════════════════════════════════════
# SLIDES 4-6 — Xuân Hương
# ════════════════════════════════════════════════════

def s4(slide):
    add_textbox(slide, "Vấn đề: API bị cô lập → Lấy dữ liệu thị trường ở đâu?",
                Inches(0.5), Inches(1.6), Inches(12), Inches(0.4),
                font_size=15, bold=True, color=GOLD)
    add_textbox(slide, "Giải pháp: Server tự đóng vai Client — gọi ra 2 nguồn API bên ngoài",
                Inches(0.5), Inches(2.1), Inches(12), Inches(0.4),
                font_size=14, color=LIGHT_GRAY, italic=True)

    # Two cards
    cards = [
        ("Binance API", "Sàn giao dịch tài sản số lớn nhất thế giới", "Giá Spot Gold PAXG\n(Open, High, Low, Volume)"),
        ("Open Exchange Rates", "Tổ chức tài chính cung cấp tỷ giá quốc tế", "Tỷ giá USD → VND\n(Thời gian thực)"),
    ]
    for i, (name, desc, data) in enumerate(cards):
        x = Inches(0.5 + i * 6.5)
        add_rect(slide, x, Inches(2.7), Inches(6), Inches(2.8), RGBColor(0x1A,0x1A,0x2E))
        add_rect(slide, x, Inches(2.7), Inches(6), Inches(0.45), GOLD)
        add_textbox(slide, name, x+Inches(0.1), Inches(2.7), Inches(5.8), Inches(0.45),
                    font_size=14, bold=True, color=BG_DARK)
        add_textbox(slide, desc, x+Inches(0.15), Inches(3.2), Inches(5.7), Inches(0.5),
                    font_size=12, color=LIGHT_GRAY, italic=True)
        add_textbox(slide, "Dữ liệu lấy về:", x+Inches(0.15), Inches(3.75), Inches(5.7), Inches(0.35),
                    font_size=12, bold=True, color=GOLD)
        add_textbox(slide, data, x+Inches(0.15), Inches(4.15), Inches(5.7), Inches(0.7),
                    font_size=13, color=WHITE)

make_content_slide("Slide 4 · Vấn Đề API Cô Lập & Giải Pháp", "Xuân Hương", s4)

def s5(slide):
    add_textbox(slide, "Luồng xử lý bên trong /realtime endpoint (bất đồng bộ):",
                Inches(0.5), Inches(1.6), Inches(12), Inches(0.4),
                font_size=15, bold=True, color=GOLD)
    add_code_block(slide,
        "1. Server gửi HTTP GET → Binance API\n   └─ Nhận JSON Klines → Trích Open, High, Low, Volume\n\n2. Server gửi HTTP GET → Exchange Rates API\n   └─ Đọc node 'VND' → Nhận tỷ giá\n\n3. Gộp 4 giá trị → Đưa vào AI Model\n   └─ AI trả về PredictedClose (USD)\n\n4. Tính: PredictedClose × VND_Rate = Giá VNĐ\n   └─ Trả về JSON cho Client",
        Inches(0.5), Inches(2.1), Inches(7))

    add_textbox(slide, "Tại sao dùng async/await?", Inches(7.8), Inches(1.6), Inches(5), Inches(0.4),
                font_size=15, bold=True, color=GOLD)
    add_bullet_block(slide, [
        "Server không bị 'đứng' khi chờ mạng.",
        "Xử lý nhiều request đồng thời.",
        "Tăng throughput tổng thể.",
        "",
        "Kỹ thuật: Task<IResult>",
        "JSON: System.Text.Json DOM tree",
        "→ Không cần map toàn bộ object,",
        "   chỉ đọc đúng node cần thiết.",
    ], Inches(7.8), Inches(2.1), Inches(5))

make_content_slide("Slide 5 · Xử Lý Bất Đồng Bộ & Phân Tích JSON", "Xuân Hương", s5)

def s6(slide):
    add_textbox(slide, "Vấn đề khi dùng new HttpClient() trực tiếp:",
                Inches(0.5), Inches(1.6), Inches(12), Inches(0.4),
                font_size=15, bold=True, color=GOLD)
    add_bullet_block(slide, [
        "Mỗi Request tạo ra một kết nối Socket mới → Cạn kiệt Port (Socket Exhaustion).",
        "Ảnh hưởng nghiêm trọng khi có hàng trăm người dùng gọi API đồng thời.",
    ], Inches(0.5), Inches(2.05), Inches(12))

    add_textbox(slide, "Giải pháp: IHttpClientFactory",
                Inches(0.5), Inches(2.9), Inches(12), Inches(0.4),
                font_size=15, bold=True, color=GOLD)
    add_bullet_block(slide, [
        "Đăng ký vào Dependency Injection Container — quản lý vòng đời bộ gọi HTTP.",
        "Tái sử dụng kết nối Socket hiệu quả → Không bao giờ bị cạn kiệt Port.",
    ], Inches(0.5), Inches(3.35), Inches(12))

    add_textbox(slide, "Cấu hình — chỉ 1 dòng trong ServiceExtensions.cs:",
                Inches(0.5), Inches(4.1), Inches(12), Inches(0.4),
                font_size=14, bold=True, color=LIGHT_GRAY)
    add_code_block(slide, "builder.Services.AddHttpClient();",
                   Inches(0.5), Inches(4.55), Inches(12))

    add_rect(slide, Inches(0.5), Inches(5.4), Inches(12.3), Inches(0.75), RGBColor(0x1A,0x1A,0x2E))
    add_textbox(slide, "💡  Thay đổi nhỏ trong DI Container, ngăn chặn toàn bộ nguy cơ Port Exhaustion khi scale.",
                Inches(0.7), Inches(5.45), Inches(12), Inches(0.65),
                font_size=14, color=ACCENT_BLUE, italic=True)

make_content_slide("Slide 6 · IHttpClientFactory - Gọi API Chuyên Nghiệp", "Xuân Hương", s6)

# ════════════════════════════════════════════════════
# SLIDES 7-9 — Văn Nguyễn
# ════════════════════════════════════════════════════

def s7(slide):
    add_textbox(slide, "Vấn đề đặc thù khi Host Machine Learning làm REST API:",
                Inches(0.5), Inches(1.6), Inches(12), Inches(0.4),
                font_size=15, bold=True, color=GOLD)
    add_bullet_block(slide, [
        "File GoldModel.zip nặng ~43MB — chứa toàn bộ cấu trúc thần kinh nhân tạo.",
        "Nếu nạp lại model mỗi lần có Request → Tốn hàng giây xử lý mỗi lượt gọi.",
        "Hàng trăm người dùng đồng thời → Memory Leak → Server Crash.",
    ], Inches(0.5), Inches(2.1), Inches(12))

    add_textbox(slide, "Kịch bản nguy hiểm:", Inches(0.5), Inches(3.2), Inches(12), Inches(0.4),
                font_size=15, bold=True, color=RGBColor(0xF8,0x71,0x71))
    add_code_block(slide,
        "// ❌ Cách sai — nạp lại model mỗi request\napp.MapPost('/predict', (input) => {\n    var ctx = new MLContext();\n    var model = ctx.Model.Load('GoldModel.zip', ...);\n    // → RAM tăng vô hạn theo số lượng request\n});",
        Inches(0.5), Inches(3.65), Inches(12))

make_content_slide("Slide 7 · Bài Toán Hiệu Năng - Hosting ML Model", "Văn Nguyễn", s7)

def s8(slide):
    add_textbox(slide, "Giải pháp: PredictionEnginePool (Object Pooling)",
                Inches(0.5), Inches(1.6), Inches(12), Inches(0.4),
                font_size=15, bold=True, color=GOLD)
    add_code_block(slide,
        "// ✅ Đăng ký 1 lần duy nhất lúc Server khởi động\nbuilder.Services.AddPredictionEnginePool<ModelInput, ModelOutput>(\n    modelName: 'GoldModel',\n    modelBuilder: ctx => ctx.Model.Load('GoldModel.zip', ...)\n);",
        Inches(0.5), Inches(2.1), Inches(12))

    add_textbox(slide, "Cơ chế hoạt động:", Inches(0.5), Inches(3.3), Inches(12), Inches(0.4),
                font_size=15, bold=True, color=GOLD)
    items_l = ["🟢  Server start → Nạp model vào RAM đúng 1 lần.", "🔄  Request đến → Mượn Engine → Dự báo → Trả lại Pool."]
    items_r = ["✅  Thread-Safe: Ngàn requests song song, không xung đột.", "✅  Zero Memory Leak: Pool tự quản lý vòng đời object."]
    add_bullet_block(slide, items_l, Inches(0.5), Inches(3.75), Inches(6.2), font_size=14)
    add_bullet_block(slide, items_r, Inches(6.8), Inches(3.75), Inches(6), font_size=14)

make_content_slide("Slide 8 · PredictionEnginePool - Quản Trị RAM", "Văn Nguyễn", s8)

def s9(slide):
    add_textbox(slide, "Nguy cơ: API công khai → Dễ bị DDoS (tấn công làm nghẽn Server)",
                Inches(0.5), Inches(1.6), Inches(12), Inches(0.4),
                font_size=15, bold=True, color=GOLD)

    add_textbox(slide, "Giải pháp: Fixed Window Rate Limiting Middleware",
                Inches(0.5), Inches(2.1), Inches(12), Inches(0.4),
                font_size=15, bold=True, color=GOLD)

    add_rect(slide, Inches(0.5), Inches(2.6), Inches(5.5), Inches(2.2), RGBColor(0x1A,0x2A,0x1A))
    add_textbox(slide, "Cấu hình hiện tại:",
                Inches(0.65), Inches(2.65), Inches(5), Inches(0.35),
                font_size=13, bold=True, color=RGBColor(0x86,0xEF,0xAC))
    add_textbox(slide, "• Permit Limit: 5 Request\n• Window: 10 giây / IP\n• Queue: 2 Request được xếp hàng",
                Inches(0.65), Inches(3.05), Inches(5.1), Inches(1.5),
                font_size=14, color=WHITE)

    add_rect(slide, Inches(6.2), Inches(2.6), Inches(6.6), Inches(2.2), RGBColor(0x2A,0x1A,0x1A))
    add_textbox(slide, "Kết quả khi vượt giới hạn:",
                Inches(6.35), Inches(2.65), Inches(6.2), Inches(0.35),
                font_size=13, bold=True, color=RGBColor(0xF8,0x71,0x71))
    add_textbox(slide, "❌  HTTP 429 Too Many Requests\n\n⚡  Bị chặn tại tầng HTTP Pipeline\n     → Chưa chạm vào AI Model\n     → CPU & RAM hoàn toàn an toàn",
                Inches(6.35), Inches(3.05), Inches(6.2), Inches(1.5),
                font_size=13, color=WHITE)

    add_rect(slide, Inches(0.5), Inches(5.4), Inches(12.3), Inches(0.75), RGBColor(0x1B,0x1B,0x2A))
    add_textbox(slide, "💡  Middleware chặn từ ngoài vào — lớp khiên thép bảo vệ toàn bộ tài nguyên phía trong.",
                Inches(0.7), Inches(5.45), Inches(12), Inches(0.65),
                font_size=14, color=ACCENT_BLUE, italic=True)

make_content_slide("Slide 9 · Rate Limiting - Tường Lửa Chống Tấn Công", "Văn Nguyễn", s9)

# ════════════════════════════════════════════════════
# SLIDES 10-12 — Quốc Đạt
# ════════════════════════════════════════════════════

def s10(slide):
    add_textbox(slide, "Vấn đề: 'Code chạy máy em, sao Server lại lỗi?' → Xung đột môi trường .NET",
                Inches(0.5), Inches(1.6), Inches(12), Inches(0.4),
                font_size=15, bold=True, color=GOLD)

    add_textbox(slide, "Giải pháp: Docker Multi-stage Build",
                Inches(0.5), Inches(2.1), Inches(6.5), Inches(0.4),
                font_size=15, bold=True, color=GOLD)
    add_code_block(slide,
        "# Stage 1: Build (SDK ~800MB)\nFROM mcr.microsoft.com/dotnet/sdk:10.0 AS build\nRUN dotnet publish -c Release -o /app/publish\n\n# Stage 2: Runtime (~200MB)\nFROM mcr.microsoft.com/dotnet/aspnet:10.0 AS final\nCOPY --from=build /app/publish .\nENTRYPOINT [\"dotnet\", \"GoldPrice_API.dll\"]",
        Inches(0.5), Inches(2.6), Inches(6.5))

    add_textbox(slide, "Kết quả:", Inches(7.2), Inches(2.1), Inches(5.6), Inches(0.4),
                font_size=15, bold=True, color=GOLD)
    add_bullet_block(slide, [
        "✅  Image production chỉ ~200MB.",
        "✅  Không chứa SDK thừa.",
        "✅  Chạy giống hệt nhau trên",
        "     mọi máy có Docker.",
        "",
        "docker compose up -d",
        "→ Toàn bộ hệ thống khởi động",
        "   chỉ với 1 lệnh duy nhất.",
    ], Inches(7.2), Inches(2.6), Inches(5.6), font_size=13)

make_content_slide("Slide 10 · Docker - Đóng Gói & Chuẩn Hóa Môi Trường", "Quốc Đạt", s10)

def s11(slide):
    add_textbox(slide, "Quy trình CI/CD tự động (GitHub Actions):",
                Inches(0.5), Inches(1.6), Inches(7), Inches(0.4),
                font_size=15, bold=True, color=GOLD)

    steps = ["git push lên GitHub", "GitHub Actions kích hoạt", "Build Docker Image", "Push lên GHCR", "Server kéo image mới → Restart"]
    arrow_x = Inches(0.7)
    t = Inches(2.1)
    for i, step in enumerate(steps):
        clr = GOLD if i == 0 else (RGBColor(0x86,0xEF,0xAC) if i == 4 else LIGHT_GRAY)
        add_rect(slide, arrow_x, t, Inches(5.8), Inches(0.5), RGBColor(0x1E,0x1E,0x1E))
        add_textbox(slide, f"{'→  ' if i>0 else '📤  '}{step}", arrow_x+Inches(0.15), t+Inches(0.05), Inches(5.5), Inches(0.4),
                    font_size=13, color=clr, bold=(i==0 or i==4))
        t += Inches(0.55)

    add_textbox(slide, "Nginx Reverse Proxy:", Inches(7.2), Inches(1.6), Inches(5.6), Inches(0.4),
                font_size=15, bold=True, color=GOLD)
    add_bullet_block(slide, [
        "Tiếp nhận traffic từ nttspace.online",
        "(Port 80 / 443 HTTPS).",
        "",
        "Chuyển tiếp vào Docker Container",
        "đang lắng nghe nội bộ.",
        "",
        "Kết quả:",
    ], Inches(7.2), Inches(2.1), Inches(5.6), font_size=13)

    add_rect(slide, Inches(7.2), Inches(5.05), Inches(5.7), Inches(0.6), GOLD)
    add_textbox(slide, "🌐  nttspace.online  —  LIVE!", Inches(7.3), Inches(5.1), Inches(5.5), Inches(0.5),
                font_size=16, bold=True, color=BG_DARK, align=PP_ALIGN.CENTER)

make_content_slide("Slide 11 · CI/CD & Triển Khai Trên nttspace.online", "Quốc Đạt", s11)

def s12(slide):
    add_textbox(slide, "Demo 1 — GET /api/v1/predictions/realtime",
                Inches(0.5), Inches(1.55), Inches(6.2), Inches(0.45),
                font_size=15, bold=True, color=GOLD)
    add_bullet_block(slide, [
        "1. Mở Swagger UI trên nttspace.online",
        "2. Chọn GET /realtime → Execute",
        "3. Server tự gọi Binance + Exchange Rates",
        "4. AI tính toán → Trả JSON:",
    ], Inches(0.5), Inches(2.05), Inches(6.2), font_size=13)
    add_code_block(slide,
        '"predictedClose": 2355.8\n"predictedCloseVnd": 120,000,000 VND',
        Inches(0.5), Inches(3.8), Inches(6.2))

    add_textbox(slide, "Demo 2 — Kiểm tra Rate Limiting",
                Inches(7.0), Inches(1.55), Inches(6), Inches(0.45),
                font_size=15, bold=True, color=GOLD)
    add_bullet_block(slide, [
        "1. Chọn POST /predictions → Execute liên tục",
        "2. Lần 1-5: Response 200 OK ✅",
        "3. Lần 6-7: Response 429 ❌",
        "   Too Many Requests",
        "→ Tường lửa hoạt động hoàn hảo!",
    ], Inches(7.0), Inches(2.05), Inches(6), font_size=13, color=LIGHT_GRAY)

    add_rect(slide, Inches(0.5), Inches(5.35), Inches(12.3), Inches(0.85), RGBColor(0x1B,0x2A,0x1B))
    add_textbox(slide, "✅  Toàn bộ hệ thống đang chạy LIVE tại  nttspace.online",
                Inches(0.7), Inches(5.4), Inches(12), Inches(0.7),
                font_size=16, bold=True, color=RGBColor(0x86,0xEF,0xAC), align=PP_ALIGN.CENTER)

make_content_slide("Slide 12 · Live Demo Trên Swagger", "Quốc Đạt", s12)

# ════════════════════════════════════════════════════
# FINAL SLIDE
# ════════════════════════════════════════════════════
def make_final_slide():
    slide = prs.slides.add_slide(BLANK)
    set_bg(slide)
    add_rect(slide, 0, 0, W, Inches(0.12), GOLD)
    add_rect(slide, 0, H - Inches(0.12), W, Inches(0.12), GOLD)

    add_textbox(slide, "CẢM ƠN THẦY CÔ & HỘI ĐỒNG!",
                Inches(1), Inches(1.0), Inches(11), Inches(1.2),
                font_size=44, bold=True, color=GOLD, align=PP_ALIGN.CENTER)

    add_textbox(slide, "Nhóm 3 xin lắng nghe câu hỏi phản biện.",
                Inches(1), Inches(2.3), Inches(11), Inches(0.6),
                font_size=18, color=LIGHT_GRAY, align=PP_ALIGN.CENTER, italic=True)

    gold_line(slide, Inches(3.1))

    members = [
        ("Thành Trung",  "Kiến trúc API & Swagger"),
        ("Xuân Hương",   "Tích hợp 3rd-Party APIs"),
        ("Văn Nguyễn",   "Hiệu năng & Bảo mật"),
        ("Quốc Đạt",     "DevOps & Live Demo"),
    ]
    col_w = Inches(3)
    for i, (name, role) in enumerate(members):
        x = Inches(0.5) + i * Inches(3.2)
        add_rect(slide, x, Inches(3.3), col_w, Inches(1.2), RGBColor(0x1A,0x1A,0x1A))
        add_rect(slide, x, Inches(3.3), col_w, Inches(0.08), GOLD)
        add_textbox(slide, name, x+Inches(0.1), Inches(3.4), col_w-Inches(0.2), Inches(0.5),
                    font_size=15, bold=True, color=WHITE)
        add_textbox(slide, role, x+Inches(0.1), Inches(3.9), col_w-Inches(0.2), Inches(0.55),
                    font_size=12, color=LIGHT_GRAY, italic=True)

    add_textbox(slide, "🌐  nttspace.online",
                Inches(1), Inches(5.1), Inches(11), Inches(0.6),
                font_size=20, bold=True, color=GOLD, align=PP_ALIGN.CENTER)

make_final_slide()

output = r"D:\Coding Space\Project\Group3\X-AURUM_Presentation.pptx"
prs.save(output)
print(f"[OK] PPTX saved: {output}")
