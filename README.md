# Universal Social Media Video & Audio Extractor API 🚀

An industrial-grade, high-performance API designed to extract direct, high-quality video streams (No Watermark), audio/soundtracks, and rich metadata from **TikTok, Instagram Reels, YouTube Shorts, X/Twitter, Facebook, Douyin, and Pinterest**.

Built with **FastAPI** and **yt-dlp**, ready for 1-click deployment and monetization on **RapidAPI Hub**.

---

## 🌟 Key Features

- **No-Watermark Extraction**: Extracts clean MP4 video URLs without watermarks for TikTok, Douyin, etc.
- **Audio & Soundtrack Extraction**: Directly returns clean MP3/M4A audio stream URLs.
- **Multi-Platform Support**: Works uniformly across TikTok, Instagram, YouTube, Twitter/X, Facebook, and more.
- **Fast Execution**: Average response time under 1.5 - 2.5 seconds (performs in-memory metadata stream extraction without downloading physical files to disk).
- **RapidAPI-Ready**: Built-in support for RapidAPI proxy secret verification (`x-rapidapi-proxy-secret`).
- **Swagger / OpenAPI Documentation**: Auto-generated interactive API documentation at `/docs`.

---

## 🛠️ Endpoints Overview

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | Service health check and supported platform overview |
| `GET` | `/api/v1/supported-platforms` | Detailed capabilities and feature list by platform |
| `POST` | `/api/v1/extract` | **Universal Extractor**: Accepts any supported video URL |
| `POST` | `/api/v1/tiktok` | Dedicated endpoint for TikTok & Douyin links |
| `POST` | `/api/v1/instagram` | Dedicated endpoint for Instagram Reels, Posts, and Videos |
| `POST` | `/api/v1/youtube` | Dedicated endpoint for YouTube Shorts & Videos |

### Example Request (`POST /api/v1/extract`)
```json
{
  "url": "https://www.tiktok.com/@username/video/1234567890"
}
```

### Example Response
```json
{
  "success": true,
  "platform": "tiktok",
  "id": "1234567890",
  "title": "Amazing viral video",
  "author": "creative_creator",
  "duration": 24,
  "thumbnail": "https://p16-sign.tiktokcdn.com/...",
  "view_count": 1450000,
  "like_count": 230000,
  "best_video_no_watermark": "https://v16-webapp-prime.tiktokcdn.com/video/mp4/...",
  "best_audio": "https://sf16-ies-music.tiktokcdn.com/music/...",
  "videos": [...],
  "audios": [...]
}
```

---

## 💻 Local Testing & Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Local Development Server
```bash
uvicorn app.main:app --reload --port 8000
```

### 3. Open Interactive Swagger UI
Open your browser and navigate to:
👉 `http://127.0.0.1:8000/docs`

You can test any real TikTok, Instagram, or YouTube link directly inside the Swagger UI!

---

## ☁️ Free Cloud Deployment ($0 Cost)

### Deploying to Render.com (Recommended Free Tier)
1. Push this project folder to your GitHub account (public or private repository).
2. Go to [Render.com](https://render.com) and click **New Web Service**.
3. Connect your GitHub repository.
4. Render will automatically detect `render.yaml` or use:
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Click **Create Web Service**. Within 2 minutes, you will receive your live HTTPS public API URL (e.g., `https://your-extractor-api.onrender.com`).

---

## 💰 How to List & Monetize on RapidAPI Hub

1. Log into your free account on [RapidAPI.com](https://rapidapi.com).
2. Click **My APIs** -> **Add New API**.
   - **API Name**: `Universal Social Media Video & Audio Extractor`
   - **Short Description**: `Extract clean No-Watermark HD video & MP3 audio streams from TikTok, Instagram Reels, YouTube Shorts, and X.`
   - **Category**: `Video & Media` or `Tools`
3. In **Target URL**, enter your Render public URL (e.g. `https://your-extractor-api.onrender.com`).
4. In **Definitions**, import the OpenAPI spec directly from your live app at `/openapi.json`.
5. In **Plans & Pricing**, set up your subscription tiers:
   - **Basic (Free)**: 50 requests / month ($0.00)
   - **Pro**: 2,500 requests / month (**$9.99 / mo**)
   - **Ultra**: 15,000 requests / month (**$29.99 / mo**)
   - **Mega**: 100,000 requests / month (**$79.99 / mo**)
6. Click **Publish**. Your API is now live to 4+ million developers worldwide! RapidAPI handles all billing, credit cards, and payouts directly to your account.
