import os
print("APIキー:", os.getenv("OPENAI_API_KEY"))

import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    SystemMessage,
    HumanMessage
)
from langchain_community import chat_models

# 専門家ごとのシステムメッセージを取得する関数
def get_system_message(role: str) -> str:
    system_messages = {
        "栄養士": "あなたはプロの栄養士です。ユーザーの健康に関する相談に対して、科学的かつ分かりやすい回答を提供してください。",
        "筋トレトレーナー": "あなたはプロのパーソナルトレーナーです。筋トレや体づくりに関する相談に対して、専門的かつ実用的なアドバイスを提供してください。"
    }
    return system_messages.get(role, "")

# LLMの応答を取得する関数
def get_response(role: str, user_input: str) -> str:
    try:
        chat = ChatOpenAI(temperature=0.7)

        # プロンプト構築
        messages = [
            SystemMessage(content=get_system_message(role)),
            HumanMessage(content=user_input)
        ]

        # 応答取得
        response = chat(messages)
        return response.content

    except Exception as e:
        return f"エラーが発生しました: {str(e)}"

# --- Streamlit アプリ ---
st.set_page_config(page_title="専門家相談アプリ", layout="centered")

st.title("専門家相談アプリ")
st.write("""
このアプリでは、質問を入力すると、選択した分野の専門家（AI）が回答してくれます。  
現在の対応専門家：
- 栄養士
- 筋トレトレーナー
""")

# 入力欄とラジオボタン
user_input = st.text_input("質問を入力してください：", placeholder="例：たんぱく質ってどれくらい摂ればいいの？")
expert_role = st.radio("専門家の種類を選んでください：", ("栄養士", "筋トレトレーナー"))

# 送信ボタン
if st.button("送信"):
    if user_input.strip() == "":
        st.warning("質問を入力してください。")
    else:
        with st.spinner("AIが考えています..."):
            response = get_response(expert_role, user_input)
        st.success("AIからの回答：")
        st.write(response)
