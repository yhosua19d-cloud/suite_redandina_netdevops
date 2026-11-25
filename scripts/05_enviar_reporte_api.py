import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")
API_URL = os.getenv("API_URL")

with open("datos/inventario_regional.json", "r", encoding="utf-8") as f:
    payload = json.load(f)

headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json",
}

resp = requests.post(API_URL, json=payload, headers=headers, timeout=15)
print(f"Status HTTP: {resp.status_code}")
print(json.dumps(resp.json(), indent=2))
