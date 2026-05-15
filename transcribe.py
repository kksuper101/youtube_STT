from pathlib import Path

import whisper


def transcribe_audio(audio_path: str, model_name: str = "base") -> str:
    """用 Whisper 將音檔轉成文字。model_name: tiny, base, small, medium, large"""
    path = Path(audio_path)
    if not path.exists():
        raise FileNotFoundError(f"找不到音檔：{path}")

    model = whisper.load_model(model_name)
    result = model.transcribe(str(path), language="zh")
    return result["text"].strip()