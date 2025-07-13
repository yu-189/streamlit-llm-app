import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

try:
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt="Hello, world!",
        max_tokens=5
    )
    print("APIキーは有効です。応答:", response.choices[0].text)
except openai.error.AuthenticationError:
    print("APIキーが無効です。")
except Exception as e:
    print("エラーが発生しました:", str(e))