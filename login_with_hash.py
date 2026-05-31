import requests
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

url = "https://script.google.com/macros/s/AKfycbzHtI57K9rvIFtS3FCUCkuuiLiHClyimHy5OjM6uCWHvCqpSrnIe6NYR18LyurTOFPi_w/exec"

payload = {
    "action": "login",
    "data": {
        "id": "U001",
        "pin": "4efba02990e4356fb31c65e1637a7162ccc4449870a4c26ccab052ffecae9d42"
    }
}

# Also try with username instead of id, just in case
payload_username = {
    "action": "login",
    "data": {
        "username": "ผู้ดูแลระบบ",
        "pin": "4efba02990e4356fb31c65e1637a7162ccc4449870a4c26ccab052ffecae9d42"
    }
}

for name, p in [("login by id", payload), ("login by username", payload_username)]:
    try:
        response = requests.post(url, json=p)
        print(f"{name} Status code:", response.status_code)
        print(f"  Response:", response.text)
    except Exception as e:
        print(f"  Error for {name}:", e)
