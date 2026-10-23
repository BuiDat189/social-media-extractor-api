from typing import List, Optional
from pydantic import BaseModel, Field, HttpUrl

class ExtractRequest(BaseModel):
    url: str = Field(..., description="The direct URL of the video (TikTok, Instagram, YouTube, etc.)", examples=["https://www.tiktok.com/@scout2015/video/6718335390845095173"])

class VideoStream(BaseModel):
    quality: str = Field(..., description="Resolution or quality label (e.g. 1080p, 720p, no-watermark)")
    format_id: Optional[str] = None
    extension: str = Field(..., description="Container format (mp4, webm)")
    url: str = Field(..., description="Direct downloadable video URL")
    filesize: Optional[int] = Field(None, description="Filesize in bytes if available")
    has_audio: bool = True

class AudioStream(BaseModel):
    quality: Optional[str] = Field(None, description="Audio bitrate or quality")
    extension: str = Field(..., description="Audio format (mp3, m4a, etc.)")
    url: str = Field(..., description="Direct downloadable audio URL")
    filesize: Optional[int] = None

class MediaResponse(BaseModel):
    success: bool = True
    platform: str = Field(..., description="Detected platform (tiktok, instagram, youtube, twitter, facebook, etc.)")
    id: str = Field(..., description="Original video ID")
    title: Optional[str] = Field(None, description="Title or caption of the video")
    description: Optional[str] = Field(None, description="Full description/caption")
    author: Optional[str] = Field(None, description="Uploader or creator username")
    author_url: Optional[str] = Field(None, description="Uploader profile URL")
    duration: Optional[int] = Field(None, description="Video duration in seconds")
    thumbnail: Optional[str] = Field(None, description="High-resolution thumbnail URL")
    view_count: Optional[int] = None
    like_count: Optional[int] = None
    comment_count: Optional[int] = None
    best_video_no_watermark: Optional[str] = Field(None, description="Direct URL of the best quality video without watermark")
    best_audio: Optional[str] = Field(None, description="Direct URL of the best audio/soundtrack")
    videos: List[VideoStream] = []
    audios: List[AudioStream] = []

class ErrorResponse(BaseModel):
    success: bool = False
    error: str
    detail: Optional[str] = None
