import requests
import json
import sys
from datetime import datetime
import time

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

valid_token = login_data.get("token")
assert valid_token is not None, "Login succeeded but token is missing"
print(f"Obtained valid admin token: {valid_token}")

# 2. Test invalid tokens (should fail or return error status)
invalid_tokens = [
    "AUTH_invalid_token",
    "invalid_token",
    "U001"
]

# Generate a unique job ID for each test run to avoid conflicts with existing records
current_time = datetime.now()
mock_job_id = current_time.strftime("SF-TEST-%Y%m%d-%H%M%S")
created_at_str = current_time.strftime("%Y-%m-%d %H:%M:%S")

for t in invalid_tokens:
    payload = {
        "action": "create",
        "token": t,
        "imageFolderId": "12FzCcoLz2w7ETwHwFuL4h278vkbKd0WB",
        "data": {
            "id": mock_job_id,
            "area": "A",
            "reporter": "Test Runner",
            "assignee": "สมชาย วงษา",
            "issue": "ปัญหาทดสอบระบบนำเข้า",
            "suggestion": "แก้ไขให้ถูกต้อง",
            "taskType": "safety",
            "status": "pending",
            "photoBefore": "",
            "createdAt": created_at_str
        }
    }
    
    print(f"Testing invalid token: '{t}'")
    response = requests.post(url, json=payload)
    resp_json = response.json()
    print(f"  Response: {resp_json}")
    # The API should return an error for invalid token
    assert resp_json.get("status") == "error", f"API unexpectedly succeeded with invalid token '{t}'"

# 3. Test valid token (should succeed)
valid_payload = {
    "action": "create",
    "token": valid_token,
    "imageFolderId": "12FzCcoLz2w7ETwHwFuL4h278vkbKd0WB",
    "data": {
        "id": mock_job_id,
        "area": "A",
        "reporter": "Test Runner",
        "assignee": "สมชาย วงษา",
        "issue": "ปัญหาทดสอบระบบนำเข้า",
        "suggestion": "แก้ไขให้ถูกต้อง",
        "taskType": "safety",
        "status": "pending",
        "photoBefore": "",
        "createdAt": created_at_str
    }
}

print(f"Testing valid token: '{valid_token}'")
response = requests.post(url, json=valid_payload)
assert response.status_code == 200, f"Request failed with status code {response.status_code}"
resp_json = response.json()
print(f"  Response: {resp_json}")
assert resp_json.get("status") == "success", f"Failed to create job with valid token: {resp_json.get('message')}"

# Server returns either {"id": ...} or {"data": {"id": ...}}
created_id = resp_json.get("id") or resp_json.get("data", {}).get("id")
if created_id is None:
    print(f"  WARNING: No 'id' in response, using mock_job_id for cleanup. Full response: {resp_json}")
    created_id = mock_job_id
assert created_id == mock_job_id, f"Expected created ID to be {mock_job_id}, got {created_id}"

# 4. Clean up the created test job
cleanup_payload = {
    "action": "delete",
    "token": valid_token,
    "data": {
        "id": mock_job_id
    }
}

print(f"Cleaning up test job '{mock_job_id}'...")
response_del = requests.post(url, json=cleanup_payload)
assert response_del.status_code == 200, f"Delete failed with status code {response_del.status_code}"
del_json = response_del.json()
print(f"  Cleanup Response: {del_json}")
assert del_json.get("status") == "success", f"Failed to delete test job: {del_json.get('message')}"
print("Cleanup complete!")
