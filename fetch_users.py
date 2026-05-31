import requests
import json

url = "https://script.google.com/macros/s/AKfycbzHtI57K9rvIFtS3FCUCkuuiLiHClyimHy5OjM6uCWHvCqpSrnIe6NYR18LyurTOFPi_w/exec"
params = {"action": "getUsers"}

try:
    response = requests.get(url, params=params)
    print("Status code:", response.status_code)
    data = response.json()
    print("Users Data:")
    print(json.dumps(data, indent=2, ensure_ascii=False))
except Exception as e:
    print("Error:", e)
