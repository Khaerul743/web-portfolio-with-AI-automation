import os
from flask import request
from dotenv import load_dotenv
load_dotenv()

def authHeader():
    api_key = request.headers.get("agent-key")
    agent_key = os.getenv("API_KEY")
    if api_key != agent_key or not api_key:
        return True