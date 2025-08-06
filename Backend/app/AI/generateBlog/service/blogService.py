import os
import requests
from dotenv import load_dotenv

load_dotenv()

def postToN8n(header, body, footer):
    # url = os.environ.get("N8N_URL")
    url = "https://a06e5af74a3a.ngrok-free.app/webhook/5e9ea2bd-0c3d-4ff2-867f-a8233b532157"
    payload = {
        "header":header,
        "body":body,
        "footer":footer
    }
    try:
        response = requests.post(url=url, json=payload)

        if response.status_code != 200:
            print(f"Error with status code {response.status_code}")
            return False
        
        return True
    except Exception as e:
        print(f"Terjadi kesalahan post: {str(e)}")
        return False

print(os.environ.get("N8N_URL"))

if __name__ == "__main__":
    postToN8n({"hook": "adakdad", "purpose": "dakjdad"},"adjkbabdkabsj", "bakjdksbdkbj")