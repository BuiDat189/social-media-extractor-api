import yt_dlp
from typing import Dict, Any, List
import re
from .models import MediaResponse, VideoStream, AudioStream

class MediaExtractor:
    @staticmethod
    def get_ydl_options() -> Dict[str, Any]:
        return {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'skip_download': True,
            'ignoreerrors': False,
            # Spoof common browser headers to avoid anti-bot blocks
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-us,en;q=0.5',
                'Sec-Fetch-Mode': 'navigate',
            }
        }

    @staticmethod
    def detect_platform(url: str, extractor_name: str) -> str:
        url_lower = url.lower()
        if 'tiktok.com' in url_lower:
            return 'tiktok'
        elif 'instagram.com' in url_lower:
            return 'instagram'
        elif 'youtube.com' in url_lower or 'youtu.be' in url_lower:
            return 'youtube'
        elif 'twitter.com' in url_lower or 'x.com' in url_lower:
            return 'twitter'
        elif 'facebook.com' in url_lower or 'fb.watch' in url_lower:
            return 'facebook'
        elif 'douyin.com' in url_lower:
            return 'douyin'
        elif 'pinterest.com' in url_lower or 'pin.it' in url_lower:
            return 'pinterest'
        elif 'reddit.com' in url_lower:
            return 'reddit'
        return extractor_name.lower() if extractor_name else 'unknown'

    @classmethod
    def extract(cls, url: str) -> MediaResponse:
        opts = cls.get_ydl_options()
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=False)
            if not info:
                raise ValueError("Could not extract media info from the provided URL.")

            # If it's a playlist or multiple entries, pick the first
            if 'entries' in info and info['entries']:
                info = info['entries'][0]

            platform = cls.detect_platform(url, info.get('extractor', ''))
            video_id = str(info.get('id', ''))
            title = info.get('title')
            description = info.get('description')
            author = info.get('uploader') or info.get('channel') or info.get('creator')
            author_url = info.get('uploader_url') or info.get('channel_url')
            duration = info.get('duration')
            thumbnail = info.get('thumbnail')
            view_count = info.get('view_count')
            like_count = info.get('like_count')
            comment_count = info.get('comment_count')

            videos: List[VideoStream] = []
            audios: List[AudioStream] = []
            best_video_url = None
            best_audio_url = None

            formats = info.get('formats', [])
            
            # Look for direct URLs in formats
            for f in formats:
                f_url = f.get('url')
                if not f_url:
                    continue

                vcodec = f.get('vcodec', 'none')
                acodec = f.get('acodec', 'none')
                ext = f.get('ext', 'mp4')
                filesize = f.get('filesize') or f.get('filesize_approx')
                resolution = f.get('resolution') or f"{f.get('width', '')}x{f.get('height', '')}"
                
                is_video = vcodec != 'none' and vcodec is not None
                is_audio = acodec != 'none' and acodec is not None

                if is_video:
                    quality_label = f.get('format_note') or resolution or 'standard'
                    videos.append(VideoStream(
                        quality=quality_label,
                        format_id=str(f.get('format_id', '')),
                        extension=ext,
                        url=f_url,
                        filesize=filesize,
                        has_audio=is_audio
                    ))
                elif is_audio and not is_video:
                    quality_label = f"{f.get('abr', '128')}kbps" if f.get('abr') else 'standard'
                    audios.append(AudioStream(
                        quality=quality_label,
                        extension=ext,
                        url=f_url,
                        filesize=filesize
                    ))

            # Pick best video (prefer formats with both audio + video, or highest direct URL)
            direct_video_candidates = [v for v in videos if v.has_audio and v.url.startswith('http')]
            if not direct_video_candidates and videos:
                direct_video_candidates = [v for v in videos if v.url.startswith('http')]

            if direct_video_candidates:
                best_video_url = direct_video_candidates[-1].url
            elif info.get('url'):
                best_video_url = info.get('url')

            # Pick best audio
            direct_audio_candidates = [a for a in audios if a.url.startswith('http')]
            if direct_audio_candidates:
                best_audio_url = direct_audio_candidates[-1].url

            return MediaResponse(
                success=True,
                platform=platform,
                id=video_id,
                title=title,
                description=description,
                author=author,
                author_url=author_url,
                duration=duration,
                thumbnail=thumbnail,
                view_count=view_count,
                like_count=like_count,
                comment_count=comment_count,
                best_video_no_watermark=best_video_url,
                best_audio=best_audio_url,
                videos=videos,
                audios=audios
            )
