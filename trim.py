import subprocess
from pathlib import Path


def trim_audio(
    input_path: str,
    start_sec: int = 0,
    duration_sec: int = 0,
    output_dir: Path | None = None,
) -> str:
    """
    裁切音訊。
    start_sec: 從第幾秒開始（0 = 從頭）
    duration_sec: 要取幾秒（0 = 不限制，取到結尾）
    回傳裁切後檔案路徑；若不需裁切則回傳原檔路徑。
    """
    src = Path(input_path)
    if not src.exists():
        raise FileNotFoundError(f"找不到音檔：{src}")

    if start_sec == 0 and duration_sec == 0:
        return str(src.resolve())

    out_dir = output_dir or src.parent
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{src.stem}_clip_{start_sec}s_{duration_sec or 'end'}s.mp3"

    cmd = ["ffmpeg", "-y", "-ss", str(start_sec), "-i", str(src)]
    if duration_sec > 0:
        cmd += ["-t", str(duration_sec)]
    cmd += ["-acodec", "copy", str(out_path)]

    subprocess.run(cmd, check=True, capture_output=True, text=True)
    return str(out_path.resolve())