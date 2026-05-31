import requests
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

url = "https://script.google.com/macros/s/AKfycbzHtI57K9rvIFtS3FCUCkuuiLiHClyimHy5OjM6uCWHvCqpSrnIe6NYR18LyurTOFPi_w/exec"
payload = {"action": "getUsers"}

try:
    print("Fetching users...")
    response = requests.post(url, json=payload)
    assert response.status_code == 200, f"Request failed with status code {response.status_code}"
    
    data = response.json()
    assert data.get("status") == "success", f"API returned error: {data.get('message')}"
    
    users = data.get("data", [])
    print(f"Users Data from POST (Found {len(users)} users):")
    if len(users) > 0:
        print(json.dumps(users[0], indent=2, ensure_ascii=False))
except Exception as e:
    print("Error:", e)
    raise e
