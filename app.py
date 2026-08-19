import streamlit as st
from google import genai

st.set_page_config(
    page_title="Gemini 測試",
    page_icon="🤖"
)

st.title("🤖 Gemini API 測試")

try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except Exception as e:
    st.error("讀取 GEMINI_API_KEY 失敗")
    st.code(repr(e))
    st.stop()

if not API_KEY:
    st.error("GEMINI_API_KEY 是空的")
    st.stop()

st.success("GEMINI_API_KEY 已讀取")

try:
    client = genai.Client(
        api_key=str(API_KEY).strip()
    )

    st.success("Gemini Client 建立成功")

except Exception as e:
    st.error("Gemini Client 建立失敗")
    st.code(repr(e))
    st.stop()


if st.button("測試 Gemini"):

    try:

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents="請只回答：測試成功"
        )

        st.success("Gemini API 正常")

        st.write(response.text)

    except Exception as e:

        st.error("Gemini API 發生錯誤")

        st.code(repr(e))

        st.write("完整錯誤：")

        st.exception(e)
