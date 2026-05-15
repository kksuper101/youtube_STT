import os
from pathlib import Path

import streamlit as st

from download import download_audio
from transcribe import transcribe_audio
from trim import trim_audio

st.set_page_config(
    page_title="YouTube 採聲器",
    page_icon="🎧",
    layout="centered",
)

UPLOAD_DIR = Path(__file__).parent / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

st.title("🎧 YouTube 採聲器")
st.caption("YouTube 下載或上傳音檔 → 裁切 → 轉成文字")

st.write("大家好")
st.write("這是我的 YouTube 採聲器專案")
st.write("單純測試用")

tab_yt, tab_upload = st.tabs(["YouTube 下載", "上傳音檔"])

with tab_yt:
    if os.environ.get("STREAMLIT_RUNTIME_ENV") == "cloud":
        st.info("youtube採聲器雲端無法使用，請至本機測試")
    url = st.text_input(
        "請貼上 YouTube 網址",
        placeholder="https://www.youtube.com/watch?v=...",
    )

    col1, col2 = st.columns(2)
    with col1:
        start_sec = st.number_input(
            "從第幾秒開始（0 = 從頭）",
            min_value=0,
            value=0,
            step=1,
            key="yt_start",
        )
    with col2:
        duration_sec = st.number_input(
            "要取幾秒（0 = 不限制，取到結尾）",
            min_value=0,
            value=0,
            step=1,
            key="yt_duration",
        )

    if st.button("開始下載音訊", key="yt_btn"):
        if not url.strip():
            st.error("請先貼上 YouTube 網址")
        else:
            try:
                with st.spinner("下載中，請稍候…"):
                    audio_path = download_audio(url.strip())
                with st.spinner("裁切中…"):
                    audio_path = trim_audio(
                        audio_path,
                        start_sec=int(start_sec),
                        duration_sec=int(duration_sec),
                    )
                st.success("處理完成！")
                st.write(f"檔案位置：`{audio_path}`")
                st.audio(audio_path, format="audio/mp3")
                with st.spinner("轉換文字中（第一次會較久）…"):
                    text = transcribe_audio(audio_path, model_name="base")
                st.subheader("逐字稿")
                st.text_area("轉錄結果", value=text, height=300, key="yt_text")
            except Exception as e:
                st.error(f"處理失敗：{e}")

with tab_upload:
    st.write("可上傳本機音檔（mp3 / wav / m4a / webm / ogg），裁切後轉成文字。")
    uploaded = st.file_uploader(
        "選擇音檔",
        type=["mp3", "wav", "m4a", "webm", "ogg"],
    )

    col3, col4 = st.columns(2)
    with col3:
        up_start = st.number_input(
            "從第幾秒開始（0 = 從頭）",
            min_value=0,
            value=0,
            step=1,
            key="up_start",
        )
    with col4:
        up_duration = st.number_input(
            "要取幾秒（0 = 不限制）",
            min_value=0,
            value=0,
            step=1,
            key="up_duration",
        )

    if st.button("開始分析上傳音檔", key="up_btn"):
        if uploaded is None:
            st.error("請先選擇音檔")
        else:
            try:
                save_path = UPLOAD_DIR / uploaded.name
                save_path.write_bytes(uploaded.getvalue())

                with st.spinner("裁切中…"):
                    audio_path = trim_audio(
                        str(save_path),
                        start_sec=int(up_start),
                        duration_sec=int(up_duration),
                    )
                st.success("處理完成！")
                st.write(f"檔案位置：`{audio_path}`")
                st.audio(audio_path)

                with st.spinner("轉換文字中（第一次會較久）…"):
                    text = transcribe_audio(audio_path, model_name="base")
                st.subheader("逐字稿")
                st.text_area("轉錄結果", value=text, height=300, key="up_text")
            except Exception as e:
                st.error(f"分析失敗：{e}")