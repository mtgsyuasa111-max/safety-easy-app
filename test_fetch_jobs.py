import requests
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

url = "https://script.google.com/macros/s/AKfycbzHtI57K9rvIFtS3FCUCkuuiLiHClyimHy5OjM6uCWHvCqpSrnIe6NYR18LyurTOFPi_w/exec"

# 1. Dynamically login as Admin to obtain valid session token
login_payload = {
    "action": "login",
    "data": {
        "id": "U001",
        "pin": "5316"
    }
}

print("Logging in dynamically...")
response_login = requests.post(url, json=login_payload)
assert response_login.status_code == 200, f"Login request failed with status code {response_login.status_code}"
login_data = response_login.json()
assert login_data.get("status") == "success", f"Login failed: {login_data.get('message')}"

token = login_data.get("token")
assert token is not None, "Login succeeded but token is missing"
print(f"Obtained valid admin token: {token}")

# 2. Query getJobs using the obtained token
params = {
    "action": "getJobs",
    "token": token
}

print("Fetching jobs list...")
response = requests.get(url, params=params)
assert response.status_code == 200, f"Fetch jobs failed with status code {response.status_code}"

data = response.json()
if isinstance(data, list):
    jobs = data
else:
    assert data.get("status") == "success", f"Failed to get jobs: {data.get('message')}"
    jobs = data.get("data", [])

print(f"Number of existing jobs in sheet: {len(jobs)}")
if len(jobs) > 0:
    print("Example Job:")
    print(json.dumps(jobs[0], indent=2, ensure_ascii=False))
