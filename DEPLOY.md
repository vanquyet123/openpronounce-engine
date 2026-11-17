# Deploy Engine — Render (miễn phí) hoặc Hugging Face Spaces (PRO)

Thư mục này chứa mọi thứ cần để host OpenPronounce (Wav2Vec2 + DTW + phone model).

## Phương án A — Render.com (miễn phí, khuyến nghị)

### 1. Tạo repo GitHub (web, không cần git CLI)

1. Vào https://github.com/new → đặt tên `openpronounce-engine` → Public → Create repository.
2. Trong repo → **Add file → Upload files** → kéo thả toàn bộ 6 file trong thư mục này (`Dockerfile`, `requirements.txt`, `server.py`, `entrypoint.py`, `README.md`, `render.yaml`) → **Commit changes**.

### 2. Deploy trên Render

1. Đăng nhập https://render.com (có thể dùng tài khoản GitHub).
2. **New → Web Service** → chọn repo `openpronounce-engine` → Connect.
3. Render tự nhận Dockerfile. Giữ mặc định:
   - Plan: **Free**
   - Health Check Path: `/health`
4. (Tuỳ chọn) Environment → thêm `OPENPRONOUNCE_API_KEY` = chuỗi bí mật.
5. **Create Web Service**. Build ~5–10 phút (lần đầu tải torch + model).
6. URL: `https://openpronounce-engine.onrender.com` (hoặc tên bạn đặt).

### 3. Cold start & giới hạn free tier

- Sleep sau 15 phút không dùng → request đầu tiên cold start ~1–2 phút.
- 512MB RAM free tier — model Wav2Vec2 có thể vượt; nếu crash, nâng lên Starter ($7/tháng) hoặc dùng VPS.
- Health check `/health` giữ service awake (Render ping mỗi 5 phút? Actually free tier không ping; service sleep).

> Tip: Để tránh sleep, dùng UptimeRobot (free) ping `/health` mỗi 5 phút.

## Phương án B — Hugging Face Spaces (cần PRO $9/tháng)

Xem phần cũ: tạo Space Docker, upload 5 file (không cần render.yaml), URL `https://<user>-<space>.hf.space`.

## Sau khi có URL — cấu hình GAS

Mở Apps Script IDE → chạy hàm `configureEngine` với tham số:
```
["https://openpronounce-engine.onrender.com", "<api-key-neu-co>"]
```

Hoặc đặt Script Property `OPENPRONOUNCE_URL` = URL (và `OPENPRONOUNCE_API_KEY` nếu có).

Kiểm tra: pill header → `Engine sẵn sàng`; ghi âm → chấm điểm → hiện điểm + âm vị.
