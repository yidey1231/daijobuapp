from openai import OpenAI
import os
from dotenv import load_dotenv

# .envファイルからAPIキーをロード
load_dotenv()
client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

# GPT-4からの応答を取得する関数
def get_gpt_response(text):
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"{text}かなり彼女に寄り添ったアドバイスを100文字程度で答えて。",
                }
            ],
            model="gpt-4o-mini",
        )
        message_content = chat_completion.choices[0].message.content
        return message_content
    except Exception as e:
        return f"エラーが発生しました: {str(e)}"