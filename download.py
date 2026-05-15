from pathlib import Path

import yt_dlp

DOWNLOAD_DIR = Path(__file__).parent / "downloads"


def download_audio(url: str) -> str:
    """下載 YouTube 音訊並轉成 mp3，回傳檔案完整路徑。"""
    DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)

    opts = {
        "format": "bestaudio/best",
        "outtmpl": str(DOWNLOAD_DIR / "%(title)s.%(ext)s"),
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        "quiet": True,
        "noplaylist": True,
    }

    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=True)
        mp3_path = Path(ydl.prepare_filename(info)).with_suffix(".mp3")

    if not mp3_path.exists():
        raise FileNotFoundError(f"找不到下載的 mp3：{mp3_path}")

    return str(mp3_path.resolve())