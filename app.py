import streamlit as st

st.set_page_config(
    page_title="YouTube 採聲器",
    page_icon="🎧",
    layout="centered",
)

st.title("🎧 YouTube 採聲器")
st.caption("第 1 步：介面測試（尚未下載音訊）")

st.write("大家好")
st.write("這是我的 YouTube 採聲器專案")
st.write("單純測試用")

url = st.text_input("請貼上 YouTube 網址", placeholder="https://www.youtube.com/watch?v=...")

col1, col2 = st.columns(2)
with col1:
    start_sec = st.number_input("從第幾秒開始（0 = 從頭）", min_value=0, value=0, step=1)
with col2:
    duration_sec = st.number_input(
        "要取幾秒（0 = 不限制，之後步驟才會真的用到）",
        min_value=0,
        value=0,
        step=1,
    )

if st.button("開始處理（第 1 步僅顯示設定）"):
    if not url.strip():
        st.error("請先貼上 YouTube 網址")
    else:
        st.success("介面正常！")
        st.json({
            "網址": url.strip(),
            "開始秒數": start_sec,
            "長度秒數": "不限制" if duration_sec == 0 else duration_sec,
        })
