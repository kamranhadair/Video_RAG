"""YouTube video downloader using yt-dlp."""
import yt_dlp
from pathlib import Path
from typing import Tuple, Optional
import hashlib
import os

class VideoDownloader:
    """Downloads audio from YouTube videos."""
    
    def __init__(self, cache_dir: Path):
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.ffmpeg_path = str(Path(__file__).parent.parent.parent / 'bin' / 'ffmpeg')
        self.ffprobe_path = str(Path(__file__).parent.parent.parent / 'bin' / 'ffprobe')
    
    def download_audio(self, url: str) -> Tuple[str, dict]:
        """Download audio from YouTube URL."""
        video_id = hashlib.md5(url.encode()).hexdigest()[:12]
        audio_path = self.cache_dir / f"{video_id}.mp3"
        
        if audio_path.exists():
            metadata = self._extract_metadata(url)
            return str(audio_path), {**metadata, 'video_id': video_id}
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': str(self.cache_dir / f'{video_id}.%(ext)s'),
            'quiet': True,
            'no_warnings': True,
            'ffmpeg_location': str(Path(__file__).parent.parent.parent / 'bin'),
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            metadata = {
                'video_id': video_id,
                'title': info.get('title', 'Unknown'),
                'duration': info.get('duration', 0),
                'url': url
            }
        
        return str(audio_path), metadata
    
    def _extract_metadata(self, url: str) -> dict:
        """Extract metadata without downloading."""
        ydl_opts = {'quiet': True, 'no_warnings': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return {
                'title': info.get('title', 'Unknown'),
                'duration': info.get('duration', 0),
                'url': url
            }
