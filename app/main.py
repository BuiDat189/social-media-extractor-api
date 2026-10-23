import os
from fastapi import FastAPI, HTTPException, Request, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from typing import Optional
from pathlib import Path

from .models import ExtractRequest, MediaResponse, ErrorResponse
from .extractor import MediaExtractor

RAPIDAPI_PROXY_SECRET = os.getenv("RAPIDAPI_PROXY_SECRET", "")
INDEX_HTML_PATH = Path(__file__).parent / "index.html"

app = FastAPI(
    title="Universal Social Media Video & Audio Extractor API",
    description="High-performance API to extract direct high-quality video (No Watermark), audio/soundtracks, and metadata from TikTok, Instagram Reels, YouTube Shorts, Twitter/X, Facebook, and more.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=[
        {"name": "Universal Extractor", "description": "Extract media from any supported social platform"},
        {"name": "Dedicated Platform Endpoints", "description": "Platform-specific shortcuts"},
        {"name": "System", "description": "Status and supported platform info"},
    ]
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def verify_rapidapi_header(request: Request, call_next):
    # If RAPIDAPI_PROXY_SECRET is configured in environment, verify it
    if RAPIDAPI_PROXY_SECRET:
        proxy_secret = request.headers.get("x-rapidapi-proxy-secret")
        # Allow open access to docs and root status
        if request.url.path not in ["/", "/docs", "/redoc", "/openapi.json"]:
            if proxy_secret != RAPIDAPI_PROXY_SECRET:
                return JSONResponse(
                    status_code=403,
                    content={"success": False, "error": "Unauthorized", "detail": "Invalid or missing RapidAPI Proxy Secret."}
                )
    return await call_next(request)

@app.get("/", tags=["System"], response_class=HTMLResponse)
async def root():
    if INDEX_HTML_PATH.exists():
        return HTMLResponse(content=INDEX_HTML_PATH.read_text(encoding="utf-8"))
    return HTMLResponse(content="<h1>Universal Social Media Extractor API is Online</h1><p>Visit <a href='/docs'>/docs</a></p>")

@app.get("/api/v1/supported-platforms", tags=["System"])
async def get_supported_platforms():
    return {
        "success": True,
        "platforms": [
            {"id": "tiktok", "name": "TikTok", "features": ["No Watermark Video", "Original Audio MP3", "Stats"]},
            {"id": "instagram", "name": "Instagram Reels & Videos", "features": ["HD MP4", "Audio Stream", "Thumbnail"]},
            {"id": "youtube", "name": "YouTube Shorts & Videos", "features": ["Multi-quality Video", "Audio Stream", "Captions"]},
            {"id": "twitter", "name": "X / Twitter", "features": ["Multi-bitrate MP4 Video"]},
            {"id": "facebook", "name": "Facebook Watch & Reels", "features": ["HD / SD Video"]},
            {"id": "douyin", "name": "Douyin", "features": ["No Watermark Video", "Audio"]},
            {"id": "pinterest", "name": "Pinterest", "features": ["Direct Video"]}
        ]
    }

@app.post(
    "/api/v1/extract", 
    response_model=MediaResponse, 
    tags=["Universal Extractor"],
    responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}}
)
async def extract_media(payload: ExtractRequest):
    """
    Extract video, audio, and metadata from any supported social media URL.
    Returns direct CDN URLs without watermarks whenever available.
    """
    if not payload.url or not payload.url.strip():
        raise HTTPException(status_code=400, detail="The 'url' parameter is required.")

    try:
        result = MediaExtractor.extract(payload.url.strip())
        return result
    except Exception as e:
        error_msg = str(e)
        raise HTTPException(
            status_code=400, 
            detail=f"Failed to extract media: {error_msg}"
        )

@app.post("/api/v1/tiktok", response_model=MediaResponse, tags=["Dedicated Platform Endpoints"])
async def extract_tiktok(payload: ExtractRequest):
    """Specific endpoint for TikTok videos (returns clean video without watermark)."""
    return await extract_media(payload)

@app.post("/api/v1/instagram", response_model=MediaResponse, tags=["Dedicated Platform Endpoints"])
async def extract_instagram(payload: ExtractRequest):
    """Specific endpoint for Instagram Reels, Posts, and Videos."""
    return await extract_media(payload)

@app.post("/api/v1/youtube", response_model=MediaResponse, tags=["Dedicated Platform Endpoints"])
async def extract_youtube(payload: ExtractRequest):
    """Specific endpoint for YouTube Shorts and YouTube videos."""
    return await extract_media(payload)
