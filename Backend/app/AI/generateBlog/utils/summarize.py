import os
import requests
from dotenv import load_dotenv

load_dotenv()


def summarize_with_gemini(text:str) -> str:
    payload = {
        "contents": [
        {
            "parts": [
            {
                "text": f"tolong ringkas text berikut minimal 1000 kata. awali kalimat 'berdasarkan jurnal dari ...': {text}"
            }
            ]
        }
        ]
    }

    headers = {
        "Content-Type":"application/json",
        "X-goog-api-key": os.environ.get("GEMINI_API_KEY")
    }
    try:
        result = requests.post(url="https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent",headers=headers,json=payload).json()
        return result["candidates"][0]["content"]["parts"][0]["text"]
    except:
        return text[:700]
    

def summarize_blog(text:str) -> str:
    payload = {
        "contents": [
        {
            "parts": [
            {
                "text": f"tolong ringkas masing masing poin dari body blog tersebut, untuk output text jangan ada simbol ini'*', berikut adalah blognya : {text}"
            }
            ]
        }
        ]
    }

    headers = {
        "Content-Type":"application/json",
        "X-goog-api-key": os.environ.get("GEMINI_API_KEY")
    }
    try:
        result = requests.post(url="https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent",headers=headers,json=payload).json()
        return result["candidates"][0]["content"]["parts"][0]["text"]
    except:
        return text

# if __name__ == "__main__":
#     print(len(text))
#     print(summarize_with_gemini(text=text))