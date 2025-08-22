import streamlit as st
import google.generativeai as genai
import os

# --- 画面のタイトル設定 ---
st.set_page_config(page_title="Gemini Chat Demo", page_icon="♊")
st.title("♊ Gemini API Chat Demo")
st.caption("Streamlit Community Cloudでデプロイしたデモアプリです。")

# --- APIキーの設定 ---
# Streamlitのsecrets機能を使ってAPIキーを安全に読み込む
try:
    api_key = st.secrets["AIzaSyAc5T0tjZQv5WakwdOQDKC-guGt_mFJx8Y"]
    genai.configure(api_key=api_key)
except Exception as e:
    st.error("⚠️ Gemini APIキーが設定されていません。")
    st.stop() # APIキーがない場合はここで処理を停止

# --- モデルの選択 ---
# model_name = "gemini-1.5-flash" # 最新の軽量モデル
model_name = "gemini-pro"
model = genai.GenerativeModel(model_name)

# --- チャット履歴の初期化 ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- チャット履歴の表示 ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- ユーザーからの入力 ---
prompt = st.chat_input("メッセージを入力してください...")

if prompt:
    # ユーザーのメッセージを履歴に追加・表示
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AIの応答を生成・表示
    with st.chat_message("model"):
        try:
            response = model.generate_content(prompt)
            response_text = response.text
            st.markdown(response_text)
            # AIの応答を履歴に追加
            st.session_state.messages.append({"role": "model", "content": response_text})
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")