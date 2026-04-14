from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

# ── PALETTE
BG_DARK     = RGBColor(0x0D, 0x0D, 0x0D)
GOLD        = RGBColor(0xF5, 0xC5, 0x18)
WHITE       = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT_GRAY  = RGBColor(0xCC, 0xCC, 0xCC)
DARK_GRAY   = RGBColor(0x33, 0x33, 0x33)
ACCENT_BLUE = RGBColor(0x3B, 0x82, 0xF6)
GREEN       = RGBColor(0x86, 0xEF, 0xAC)
RED_SOFT    = RGBColor(0xF8, 0x71, 0x71)

W = Inches(13.33)
H = Inches(7.5)

prs = Presentation()
prs.slide_width  = W
prs.slide_height = H
BLANK = prs.slide_layouts[6]

# ── HELPERS
def set_bg(slide):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = BG_DARK

def add_rect(slide, l, t, w, h, color):
    s = slide.shapes.add_shape(1, l, t, w, h)
    s.fill.solid(); s.fill.fore_color.rgb = color
    s.line.fill.background()
    return s

def add_tb(slide, text, l, t, w, h, size=14, bold=False,
           color=WHITE, align=PP_ALIGN.LEFT, italic=False):
    tb = slide.shapes.add_textbox(l, t, w, h)
    tb.word_wrap = True
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.alignment = align
    r = p.add_run(); r.text = text
    r.font.size = Pt(size); r.font.bold = bold
    r.font.italic = italic; r.font.color.rgb = color
    return tb

def gold_line(slide, t):
    add_rect(slide, 0, t, W, Inches(0.04), GOLD)

def bullets(slide, items, l, t, w, size=14, color=LIGHT_GRAY):
    lh = Inches(0.4)
    for item in items:
        prefix = "  *  " if not item.startswith("    ") else "       - "
        add_tb(slide, prefix + item.strip(), l, t, w, lh, size=size, color=color)
        t += lh
    return t

def code_block(slide, code, l, t, w):
    lines = code.strip().split("\n")
    h = Inches(0.3) * len(lines) + Inches(0.2)
    add_rect(slide, l, t, w, h, DARK_GRAY)
    add_tb(slide, code.strip(), l+Inches(0.1), t+Inches(0.08),
           w-Inches(0.2), h, size=11, color=GOLD)
    return t + h

def content_slide(title, speaker, fn):
    slide = prs.slides.add_slide(BLANK)
    set_bg(slide)
    add_rect(slide, 0, 0, W, Inches(0.08), GOLD)
    add_rect(slide, 0, Inches(0.08), Inches(3.0), Inches(0.42), RGBColor(0x1E,0x1E,0x1E))
    add_tb(slide, "  " + speaker, Inches(0.05), Inches(0.08), Inches(2.9), Inches(0.42),
           size=11, color=GOLD)
    add_tb(slide, title, Inches(0.5), Inches(0.62), Inches(12.3), Inches(0.75),
           size=26, bold=True, color=WHITE)
    gold_line(slide, Inches(1.42))
    fn(slide)
    return slide

# ═══════════════════════════════════════
# TITLE SLIDE
# ═══════════════════════════════════════
def title_slide():
    slide = prs.slides.add_slide(BLANK)
    set_bg(slide)
    add_rect(slide, 0, 0, W, Inches(0.12), GOLD)
    add_rect(slide, 0, H-Inches(0.12), W, Inches(0.12), GOLD)
    add_tb(slide, "X-AURUM", Inches(1), Inches(1.1), Inches(11), Inches(1.4),
           size=72, bold=True, color=GOLD, align=PP_ALIGN.CENTER)
    add_tb(slide, "He Thong Du Bao Gia Vang Theo Thoi Gian Thuc",
           Inches(1), Inches(2.65), Inches(11), Inches(0.75),
           size=22, color=WHITE, align=PP_ALIGN.CENTER)
    add_tb(slide, "Trien khai Web API tich hop Tri tue Nhan tao & Du lieu Thi truong Toan cau",
           Inches(1), Inches(3.35), Inches(11), Inches(0.6),
           size=15, color=LIGHT_GRAY, italic=True, align=PP_ALIGN.CENTER)
    gold_line(slide, Inches(4.1))
    add_tb(slide, "Nhom 3  |  Xuan Huong  |  Quoc Dat  |  Van Nguyen  |  Thanh Trung",
           Inches(1), Inches(4.3), Inches(11), Inches(0.55),
           size=15, color=LIGHT_GRAY, align=PP_ALIGN.CENTER)
    add_tb(slide, "nttspace.online", Inches(1), Inches(5.0), Inches(11), Inches(0.55),
           size=14, color=GOLD, italic=True, align=PP_ALIGN.CENTER)

title_slide()

# ═══════════════════════════════════════
# SLIDES 1-3: Xuan Huong — API Provisioning
# ═══════════════════════════════════════
def s1(slide):
    add_tb(slide, "Van de dat ra", Inches(0.5), Inches(1.58), Inches(6), Inches(0.38),
           size=15, bold=True, color=GOLD)
    bullets(slide, [
        "Mo hinh AI (ML.NET) chi chay duoc tren Console noi bo.",
        "Khong the chia se hoac tai su dung tu ben ngoai.",
    ], Inches(0.5), Inches(2.0), Inches(5.8))
    add_tb(slide, "Giai phap: ASP.NET Core Minimal API (.NET 10)", Inches(0.5), Inches(2.9), Inches(6), Inches(0.38),
           size=15, bold=True, color=GOLD)
    bullets(slide, [
        "Boc thuat toan AI thanh Web Service chuan HTTP.",
        "Loai bo Controllers truyen thong — Microservices tinh gon nhat.",
    ], Inches(0.5), Inches(3.32), Inches(5.8))
    add_tb(slide, "Clean Architecture", Inches(7), Inches(1.58), Inches(5.8), Inches(0.38),
           size=15, bold=True, color=GOLD)
    code_block(slide,
        "GoldPrice_API/\n"
        "  Endpoints/  -> Dinh tuyen API Routes\n"
        "  Models/     -> Input / Output Schema\n"
        "  Extensions/ -> DI, RateLimit, ML Pool",
        Inches(7), Inches(2.0), Inches(5.8))

content_slide("Slide 1 - Bai Toan & Kien Truc Cot Loi", "Xuan Huong", s1)

def s2(slide):
    cols_x = [Inches(0.5), Inches(3.8), Inches(7.6)]
    col_w  = [Inches(3.3), Inches(1.8), Inches(5.0)]
    hdrs   = ["Endpoint", "Method", "Mo ta"]
    for i, (x, hdr) in enumerate(zip(cols_x, hdrs)):
        add_rect(slide, x, Inches(1.58), col_w[i], Inches(0.4), GOLD)
        add_tb(slide, hdr, x+Inches(0.05), Inches(1.58), col_w[i], Inches(0.4),
               size=13, bold=True, color=BG_DARK)
    rows = [
        ["/api/v1/predictions",          "POST", "Client tu nhap du lieu OHLCV"],
        ["/api/v1/predictions/realtime", "GET",  "Bot tu keo data — khong can input"],
    ]
    for r, row in enumerate(rows):
        bg = RGBColor(0x1A,0x1A,0x1A) if r % 2 == 0 else RGBColor(0x22,0x22,0x22)
        for i, (x, cell) in enumerate(zip(cols_x, row)):
            add_rect(slide, x, Inches(1.98+r*0.45), col_w[i], Inches(0.45), bg)
            clr = GOLD if i == 1 else LIGHT_GRAY
            add_tb(slide, cell, x+Inches(0.05), Inches(1.98+r*0.45), col_w[i], Inches(0.45),
                   size=12, color=clr)
    add_tb(slide, "Chuan hoa Response RESTful (JSON Wrapper)", Inches(0.5), Inches(3.1), Inches(6.5), Inches(0.38),
           size=14, bold=True, color=GOLD)
    code_block(slide,
        '{\n'
        '  "success": true,\n'
        '  "data": {\n'
        '    "predictedClose": 2355.8,\n'
        '    "predictedCloseVnd": 120000000,\n'
        '    "liveWorldPrice": 2341.2\n'
        '  }\n'
        '}',
        Inches(0.5), Inches(3.52), Inches(6.5))
    bullets(slide, [
        "Moi Client deu parse an toan.",
        "De mo rong them truong moi.",
        "Phan biet ro luong Manual vs Auto.",
    ], Inches(7.3), Inches(3.12), Inches(5.6), size=14)

content_slide("Slide 2 - Thiet Ke Hai Luong Endpoint", "Xuan Huong", s2)

def s3(slide):
    add_tb(slide, "Tai sao can Swagger / OpenAPI?", Inches(0.5), Inches(1.58), Inches(12), Inches(0.38),
           size=15, bold=True, color=GOLD)
    bullets(slide, [
        "API dua ra ngoai ma khong co mo ta -> Ben thu 3 khong biet cach dung.",
        "OpenAPI la chuan mo ta API duoc ca nganh cong nghiep su dung.",
        "Swagger UI tu dong doc code C# -> Sinh trang tai lieu tuong tac day du.",
    ], Inches(0.5), Inches(2.0), Inches(12.3))
    add_tb(slide, "Tinh nang da tich hop", Inches(0.5), Inches(3.25), Inches(12), Inches(0.38),
           size=15, bold=True, color=GOLD)
    bullets(slide, [
        "Hien thi day du 2 endpoints, mo ta tham so va response schema.",
        "Cho phep Execute request ngay tren giao dien Web — khong can Postman.",
        "La cong cu Demo truc tiep trong buoi bao cao hom nay.",
    ], Inches(0.5), Inches(3.67), Inches(12.3))
    add_rect(slide, Inches(0.5), Inches(5.4), Inches(12.3), Inches(0.72), RGBColor(0x1B,0x2A,0x1B))
    add_tb(slide, "Swagger chinh la cong giao tiep giua nhom va the gioi ben ngoai.",
           Inches(0.7), Inches(5.45), Inches(12), Inches(0.62),
           size=14, color=GREEN, italic=True, align=PP_ALIGN.CENTER)

content_slide("Slide 3 - Tai Lieu API Tu Dong Voi Swagger (OpenAPI)", "Xuan Huong", s3)

# ═══════════════════════════════════════
# SLIDES 4-6: Quoc Dat — 3rd-Party APIs
# ═══════════════════════════════════════
def s4(slide):
    add_tb(slide, "Bai thi 3: Su dung API tu nguon ben ngoai (3rd-Party APIs)",
           Inches(0.5), Inches(1.58), Inches(12.3), Inches(0.42),
           size=16, bold=True, color=GOLD)
    add_tb(slide, "Server khong cho User nhap lieu — tu dong goi ra 2 nguon du lieu thuc te:",
           Inches(0.5), Inches(2.05), Inches(12.3), Inches(0.35),
           size=13, color=LIGHT_GRAY, italic=True)

    # Card Binance
    add_rect(slide, Inches(0.5), Inches(2.5), Inches(6.0), Inches(3.2), RGBColor(0x12,0x12,0x28))
    add_rect(slide, Inches(0.5), Inches(2.5), Inches(6.0), Inches(0.42), GOLD)
    add_tb(slide, "1. Binance Public API", Inches(0.6), Inches(2.5), Inches(5.8), Inches(0.42),
           size=14, bold=True, color=BG_DARK)
    add_tb(slide, "Muc dich: Lay gia Vang Spot theo phien giao dich",
           Inches(0.65), Inches(2.97), Inches(5.7), Inches(0.35), size=12, color=LIGHT_GRAY, italic=True)
    add_tb(slide, "HTTP Method & URL:", Inches(0.65), Inches(3.36), Inches(5.7), Inches(0.3),
           size=11, bold=True, color=GOLD)
    code_block(slide,
        "GET api.binance.com/api/v3/klines\n"
        "  ?symbol=PAXGUSDT&interval=1d&limit=1",
        Inches(0.65), Inches(3.7), Inches(5.7))
    add_tb(slide, "Trich xuat: Open, High, Low, Volume (tu mang Klines JSON)",
           Inches(0.65), Inches(4.45), Inches(5.7), Inches(0.35), size=12, color=GREEN)

    # Card Exchange Rates
    add_rect(slide, Inches(7.0), Inches(2.5), Inches(6.0), Inches(3.2), RGBColor(0x12,0x12,0x28))
    add_rect(slide, Inches(7.0), Inches(2.5), Inches(6.0), Inches(0.42), GOLD)
    add_tb(slide, "2. Open Exchange Rates API", Inches(7.1), Inches(2.5), Inches(5.8), Inches(0.42),
           size=14, bold=True, color=BG_DARK)
    add_tb(slide, "Muc dich: Lay ty gia USD -> VND hien tai",
           Inches(7.15), Inches(2.97), Inches(5.7), Inches(0.35), size=12, color=LIGHT_GRAY, italic=True)
    add_tb(slide, "HTTP Method & URL:", Inches(7.15), Inches(3.36), Inches(5.7), Inches(0.3),
           size=11, bold=True, color=GOLD)
    code_block(slide,
        "GET open.er-api.com/v6/latest/USD",
        Inches(7.15), Inches(3.7), Inches(5.7))
    add_tb(slide, "Trich xuat: rates.VND (tu object JSON phan hoi)",
           Inches(7.15), Inches(4.45), Inches(5.7), Inches(0.35), size=12, color=GREEN)

    add_rect(slide, Inches(0.5), Inches(5.85), Inches(12.5), Inches(0.62), RGBColor(0x1B,0x2A,0x1B))
    add_tb(slide, "Ket qua: PredictedClose (USD)  x  ty gia VND  =  Gia Vang VND hien tai",
           Inches(0.7), Inches(5.9), Inches(12.2), Inches(0.52),
           size=14, bold=True, color=GREEN, align=PP_ALIGN.CENTER)

content_slide("Slide 4 - Tich Hop API Ben Thu 3 (Binance & ExchangeRate)", "Quoc Dat", s4)

def s5(slide):
    add_tb(slide, "Luong xu ly ben trong /realtime endpoint (bat dong bo):",
           Inches(0.5), Inches(1.58), Inches(12.3), Inches(0.38),
           size=15, bold=True, color=GOLD)
    code_block(slide,
        "1. Server gui HTTP GET -> Binance API\n"
        "   -> Nhan JSON Klines -> Trich Open, High, Low, Volume\n\n"
        "2. Server gui HTTP GET -> Exchange Rates API\n"
        "   -> Doc node 'VND' -> Nhan ty gia\n\n"
        "3. Gop 4 gia tri -> Dua vao AI Model\n"
        "   -> AI tra ve PredictedClose (USD)\n\n"
        "4. Tinh: PredictedClose x VND_Rate = Gia VND\n"
        "   -> Tra ve JSON cho Client",
        Inches(0.5), Inches(2.0), Inches(7.0))
    add_tb(slide, "Tai sao dung async/await?", Inches(7.8), Inches(1.58), Inches(5.1), Inches(0.38),
           size=15, bold=True, color=GOLD)
    bullets(slide, [
        "Server khong bi 'dung' khi cho mang.",
        "Xu ly nhieu request dong thoi.",
        "Tang throughput tong the.",
        "",
        "Ky thuat: Task<IResult>",
        "JSON: System.Text.Json DOM tree",
        "-> Chi doc dung node can thiet,",
        "   khong map toan bo object.",
    ], Inches(7.8), Inches(2.0), Inches(5.1), size=13)

content_slide("Slide 5 - Xu Ly Bat Dong Bo & Phan Tich JSON", "Quoc Dat", s5)

def s6(slide):
    add_tb(slide, "Van de khi dung new HttpClient() truc tiep:",
           Inches(0.5), Inches(1.58), Inches(12.3), Inches(0.38),
           size=15, bold=True, color=GOLD)
    bullets(slide, [
        "Moi Request tao ra mot ket noi Socket moi -> Can kiet Port (Socket Exhaustion).",
        "Anh huong nghiem trong khi co hang tram nguoi dung goi API dong thoi.",
    ], Inches(0.5), Inches(2.0), Inches(12.3))
    add_tb(slide, "Giai phap: IHttpClientFactory",
           Inches(0.5), Inches(2.85), Inches(12.3), Inches(0.38),
           size=15, bold=True, color=GOLD)
    bullets(slide, [
        "Dang ky vao Dependency Injection Container — quan ly vong doi bo goi HTTP.",
        "Tai su dung ket noi Socket hieu qua -> Khong bao gio bi can kiet Port.",
    ], Inches(0.5), Inches(3.27), Inches(12.3))
    add_tb(slide, "Cau hinh — chi 1 dong trong ServiceExtensions.cs:",
           Inches(0.5), Inches(4.05), Inches(12.3), Inches(0.35),
           size=13, bold=True, color=LIGHT_GRAY)
    code_block(slide, "builder.Services.AddHttpClient();",
               Inches(0.5), Inches(4.44), Inches(12.3))
    add_rect(slide, Inches(0.5), Inches(5.4), Inches(12.3), Inches(0.72), RGBColor(0x1A,0x1A,0x2E))
    add_tb(slide, "Thay doi nho trong DI Container, ngan chan toan bo nguy co Port Exhaustion khi scale.",
           Inches(0.7), Inches(5.45), Inches(12), Inches(0.62),
           size=14, color=ACCENT_BLUE, italic=True, align=PP_ALIGN.CENTER)

content_slide("Slide 6 - IHttpClientFactory - Goi API Chuyen Nghiep", "Quoc Dat", s6)

# ═══════════════════════════════════════
# SLIDES 7-9: Van Nguyen — Memory & Security
# ═══════════════════════════════════════
def s7(slide):
    add_tb(slide, "Van de dac thu khi Host Machine Learning lam REST API:",
           Inches(0.5), Inches(1.58), Inches(12.3), Inches(0.38),
           size=15, bold=True, color=GOLD)
    bullets(slide, [
        "File GoldModel.zip nang ~43MB — chua toan bo cau truc than kinh nhan tao.",
        "Neu nap lai model moi lan co Request -> Ton hang giay xu ly moi luot goi.",
        "Hang tram nguoi dung dong thoi -> Memory Leak -> Server Crash.",
    ], Inches(0.5), Inches(2.0), Inches(12.3))
    add_tb(slide, "Kich ban nguy hiem:", Inches(0.5), Inches(3.2), Inches(12.3), Inches(0.38),
           size=15, bold=True, color=RED_SOFT)
    code_block(slide,
        "// WRONG — nap lai model moi request\n"
        "app.MapPost('/predict', (input) => {\n"
        "    var ctx = new MLContext();\n"
        "    var model = ctx.Model.Load('GoldModel.zip', ...);\n"
        "    // -> RAM tang vo han theo so luong request\n"
        "});",
        Inches(0.5), Inches(3.62), Inches(12.3))

content_slide("Slide 7 - Bai Toan Hieu Nang - Hosting ML Model", "Van Nguyen", s7)

def s8(slide):
    add_tb(slide, "Giai phap: PredictionEnginePool (Object Pooling)",
           Inches(0.5), Inches(1.58), Inches(12.3), Inches(0.38),
           size=15, bold=True, color=GOLD)
    code_block(slide,
        "// CORRECT — dang ky 1 lan duy nhat luc Server khoi dong\n"
        "builder.Services.AddPredictionEnginePool<ModelInput, ModelOutput>(\n"
        "    modelName: 'GoldModel',\n"
        "    modelBuilder: ctx => ctx.Model.Load('GoldModel.zip', ...)\n"
        ");",
        Inches(0.5), Inches(2.0), Inches(12.3))
    add_tb(slide, "Co che hoat dong:", Inches(0.5), Inches(3.28), Inches(12.3), Inches(0.38),
           size=15, bold=True, color=GOLD)
    bullets(slide, [
        "Server start -> Nap model vao RAM dung 1 lan.",
        "Request den -> Muon Engine -> Du bao -> Tra lai Pool.",
    ], Inches(0.5), Inches(3.7), Inches(6.2), size=14)
    bullets(slide, [
        "Thread-Safe: Ngan requests song song, khong xung dot.",
        "Zero Memory Leak: Pool tu quan ly vong doi object.",
    ], Inches(6.8), Inches(3.7), Inches(6.1), size=14)

content_slide("Slide 8 - PredictionEnginePool - Quan Tri RAM", "Van Nguyen", s8)

def s9(slide):
    add_tb(slide, "Nguy co: API cong khai -> De bi DDoS (tan cong lam nghen Server)",
           Inches(0.5), Inches(1.58), Inches(12.3), Inches(0.38),
           size=15, bold=True, color=GOLD)
    add_tb(slide, "Giai phap: Fixed Window Rate Limiting Middleware",
           Inches(0.5), Inches(2.05), Inches(12.3), Inches(0.38),
           size=15, bold=True, color=GOLD)
    add_rect(slide, Inches(0.5), Inches(2.55), Inches(5.7), Inches(2.2), RGBColor(0x1A,0x2A,0x1A))
    add_tb(slide, "Cau hinh hien tai:", Inches(0.65), Inches(2.62), Inches(5.3), Inches(0.35),
           size=13, bold=True, color=GREEN)
    add_tb(slide, "  Permit Limit: 5 Request\n  Window: 10 giay / IP\n  Queue: 2 Request duoc xep hang",
           Inches(0.65), Inches(3.02), Inches(5.3), Inches(1.5), size=14, color=WHITE)
    add_rect(slide, Inches(6.5), Inches(2.55), Inches(6.3), Inches(2.2), RGBColor(0x2A,0x1A,0x1A))
    add_tb(slide, "Ket qua khi vuot gioi han:", Inches(6.65), Inches(2.62), Inches(5.9), Inches(0.35),
           size=13, bold=True, color=RED_SOFT)
    add_tb(slide, "  HTTP 429 Too Many Requests\n\n  Bi chan tai tang HTTP Pipeline\n  -> Chua cham vao AI Model\n  -> CPU & RAM hoan toan an toan",
           Inches(6.65), Inches(3.02), Inches(5.9), Inches(1.5), size=13, color=WHITE)
    add_rect(slide, Inches(0.5), Inches(5.4), Inches(12.3), Inches(0.72), RGBColor(0x1B,0x1B,0x2A))
    add_tb(slide, "Middleware chan tu ngoai vao — lop khien thep bao ve toan bo tai nguyen phia trong.",
           Inches(0.7), Inches(5.45), Inches(12), Inches(0.62),
           size=14, color=ACCENT_BLUE, italic=True, align=PP_ALIGN.CENTER)

content_slide("Slide 9 - Rate Limiting - Tuong Lua Chong Tan Cong", "Van Nguyen", s9)

# ═══════════════════════════════════════
# SLIDES 10-12: Thanh Trung — DevOps & Demo
# ═══════════════════════════════════════
def s10(slide):
    add_tb(slide, "Van de: 'Code chay may em, sao Server lai loi?' -> Xung dot moi truong .NET",
           Inches(0.5), Inches(1.58), Inches(12.3), Inches(0.38),
           size=15, bold=True, color=GOLD)
    add_tb(slide, "Giai phap: Docker Multi-stage Build",
           Inches(0.5), Inches(2.05), Inches(6.5), Inches(0.38),
           size=15, bold=True, color=GOLD)
    code_block(slide,
        "# Stage 1: Build (SDK ~800MB)\n"
        "FROM mcr.microsoft.com/dotnet/sdk:10.0 AS build\n"
        "RUN dotnet publish -c Release -o /app/publish\n\n"
        "# Stage 2: Runtime (~200MB)\n"
        "FROM mcr.microsoft.com/dotnet/aspnet:10.0 AS final\n"
        "COPY --from=build /app/publish .\n"
        'ENTRYPOINT ["dotnet", "GoldPrice_API.dll"]',
        Inches(0.5), Inches(2.47), Inches(6.5))
    add_tb(slide, "Ket qua:", Inches(7.2), Inches(2.05), Inches(5.7), Inches(0.38),
           size=15, bold=True, color=GOLD)
    bullets(slide, [
        "Image production chi ~200MB.",
        "Khong chua SDK thua.",
        "Chay giong het nhau tren moi may co Docker.",
        "",
        "docker compose up -d",
        "-> Toan bo he thong khoi dong",
        "   chi voi 1 lenh duy nhat.",
    ], Inches(7.2), Inches(2.47), Inches(5.7), size=13)

content_slide("Slide 10 - Docker - Dong Goi & Chuan Hoa Moi Truong", "Thanh Trung", s10)

def s11(slide):
    add_tb(slide, "Quy trinh CI/CD tu dong (GitHub Actions):",
           Inches(0.5), Inches(1.58), Inches(7), Inches(0.38), size=15, bold=True, color=GOLD)
    steps = [
        "git push len GitHub",
        "GitHub Actions kich hoat",
        "Build Docker Image",
        "Push len GHCR (GitHub Container Registry)",
        "Server keo image moi & Restart",
    ]
    t = Inches(2.05)
    for i, step in enumerate(steps):
        clr = GOLD if i == 0 else (GREEN if i == 4 else LIGHT_GRAY)
        add_rect(slide, Inches(0.7), t, Inches(5.8), Inches(0.48), RGBColor(0x1E,0x1E,0x1E))
        prefix = " >> " if i > 0 else " [PUSH] "
        add_tb(slide, prefix + step, Inches(0.85), t+Inches(0.05), Inches(5.5), Inches(0.38),
               size=13, color=clr, bold=(i == 0 or i == 4))
        t += Inches(0.53)
    add_tb(slide, "Nginx Reverse Proxy:", Inches(7.2), Inches(1.58), Inches(5.7), Inches(0.38),
           size=15, bold=True, color=GOLD)
    bullets(slide, [
        "Tiep nhan traffic tu nttspace.online",
        "(Port 80 / 443 HTTPS).",
        "",
        "Chuyen tiep vao Docker Container",
        "dang lang nghe noi bo.",
        "",
        "Ket qua:",
    ], Inches(7.2), Inches(2.05), Inches(5.7), size=13)
    add_rect(slide, Inches(7.2), Inches(5.05), Inches(5.7), Inches(0.58), GOLD)
    add_tb(slide, "nttspace.online  --  LIVE!", Inches(7.3), Inches(5.1), Inches(5.5), Inches(0.48),
           size=16, bold=True, color=BG_DARK, align=PP_ALIGN.CENTER)

content_slide("Slide 11 - CI/CD & Trien Khai Tren nttspace.online", "Thanh Trung", s11)

def s12(slide):
    add_tb(slide, "Demo 1 -- GET /api/v1/predictions/realtime",
           Inches(0.5), Inches(1.55), Inches(6.2), Inches(0.42),
           size=15, bold=True, color=GOLD)
    bullets(slide, [
        "1. Mo Swagger UI tren nttspace.online",
        "2. Chon GET /realtime -> Execute",
        "3. Server tu goi Binance + Exchange Rates",
        "4. AI tinh toan -> Tra JSON:",
    ], Inches(0.5), Inches(2.02), Inches(6.2), size=13)
    code_block(slide,
        '"predictedClose": 2355.8\n'
        '"predictedCloseVnd": 120,000,000 VND',
        Inches(0.5), Inches(3.75), Inches(6.2))
    add_tb(slide, "Demo 2 -- Kiem tra Rate Limiting",
           Inches(7.0), Inches(1.55), Inches(6.0), Inches(0.42),
           size=15, bold=True, color=GOLD)
    bullets(slide, [
        "1. Chon POST /predictions -> Execute lien tuc",
        "2. Lan 1-5: Response 200 OK [OK]",
        "3. Lan 6-7: Response 429 [FAIL]",
        "   Too Many Requests",
        "-> Tuong lua hoat dong hoan hao!",
    ], Inches(7.0), Inches(2.02), Inches(6.0), size=13, color=LIGHT_GRAY)
    add_rect(slide, Inches(0.5), Inches(5.35), Inches(12.3), Inches(0.82), RGBColor(0x1B,0x2A,0x1B))
    add_tb(slide, "Toan bo he thong dang chay LIVE tai  nttspace.online",
           Inches(0.7), Inches(5.4), Inches(12), Inches(0.72),
           size=16, bold=True, color=GREEN, align=PP_ALIGN.CENTER)

content_slide("Slide 12 - Live Demo Tren Swagger", "Thanh Trung", s12)

# ═══════════════════════════════════════
# FINAL SLIDE
# ═══════════════════════════════════════
def final_slide():
    slide = prs.slides.add_slide(BLANK)
    set_bg(slide)
    add_rect(slide, 0, 0, W, Inches(0.12), GOLD)
    add_rect(slide, 0, H-Inches(0.12), W, Inches(0.12), GOLD)
    add_tb(slide, "CAM ON THAY CO & HOI DONG!",
           Inches(1), Inches(1.0), Inches(11), Inches(1.2),
           size=44, bold=True, color=GOLD, align=PP_ALIGN.CENTER)
    add_tb(slide, "Nhom 3 xin lang nghe cau hoi phan bien.",
           Inches(1), Inches(2.3), Inches(11), Inches(0.58),
           size=18, color=LIGHT_GRAY, italic=True, align=PP_ALIGN.CENTER)
    gold_line(slide, Inches(3.08))
    members = [
        ("Xuan Huong",  "Kien truc API & Swagger"),
        ("Quoc Dat",    "Tich hop 3rd-Party APIs"),
        ("Van Nguyen",  "Hieu nang & Bao mat"),
        ("Thanh Trung", "DevOps & Live Demo"),
    ]
    col_w = Inches(3.1)
    for i, (name, role) in enumerate(members):
        x = Inches(0.35) + i * Inches(3.25)
        add_rect(slide, x, Inches(3.28), col_w, Inches(1.18), RGBColor(0x1A,0x1A,0x1A))
        add_rect(slide, x, Inches(3.28), col_w, Inches(0.08), GOLD)
        add_tb(slide, name, x+Inches(0.1), Inches(3.38), col_w-Inches(0.2), Inches(0.48),
               size=15, bold=True, color=WHITE)
        add_tb(slide, role, x+Inches(0.1), Inches(3.88), col_w-Inches(0.2), Inches(0.52),
               size=12, color=LIGHT_GRAY, italic=True)
    add_tb(slide, "nttspace.online",
           Inches(1), Inches(5.08), Inches(11), Inches(0.58),
           size=20, bold=True, color=GOLD, align=PP_ALIGN.CENTER)

final_slide()

output = r"D:\Coding Space\Project\Group3\X-AURUM_Presentation.pptx"
prs.save(output)
print("[OK] PPTX saved: " + output)
