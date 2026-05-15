from transcribe import transcribe_audio
from trim import trim_audio
import streamlit as st

from download import download_audio

st.set_page_config(
    page_title="YouTube 採聲器",
    page_icon="🎧",
    layout="centered",
)

st.title("🎧 YouTube 採聲器")
st.caption("第 5 步：下載、裁切並轉成文字")

st.write("大家好")
st.write("這是我的 YouTube 採聲器專案")
st.write("單純測試用")

url = st.text_input("請貼上 YouTube 網址", placeholder="https://www.youtube.com/watch?v=...")

col1, col2 = st.columns(2)
with col1:
    start_sec = st.number_input("從第幾秒開始（0 = 從頭）", min_value=0, value=0, step=1)
with col2:
    duration_sec = st.number_input(
        "要取幾秒（0 = 不限制，取到結尾）",
        min_value=0,
        value=0,
        step=1,
    )

if st.button("開始下載音訊"):
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
            st.text_area("轉錄結果", value=text, height=300)
        except Exception as e:
            st.error(f"下載失敗：{e}")