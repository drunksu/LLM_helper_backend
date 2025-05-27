import requests
import json

# API配置
API_URL = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"
API_KEY = "c6b9d031-91ba-48a8-8d9a-9dbe6a8dc339"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

# 初始化对话上下文
messages = [
    {"role": "system", "content": "you are a helpful assistant."}
]

def answer(question: str) -> str:

    messages.append({"role": "user", "content": question})

    payload = {
        "model": "deepseek-r1-250120",
        "messages": messages,
        "stream": False
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status() 
        data = response.json()
        reply_content = data["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        reply_content = f"[错误]: 请求失败，原因: {e}"
    except (KeyError, IndexError) as e:
        reply_content = f"[错误]: 数据解析失败，原因: {e}"


    messages.append({"role": "assistant", "content": reply_content})

    return reply_content