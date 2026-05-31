import requests
import json
import sys
import time
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

url = "https://script.google.com/macros/s/AKfycbzHtI57K9rvIFtS3FCUCkuuiLiHClyimHy5OjM6uCWHvCqpSrnIe6NYR18LyurTOFPi_w/exec"

# 1. Dynamically login as Admin to obtain valid session token
login_payload = {
    "action": "login",
    "data": {
        "id": "U001",
        "pin": "9999"
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

# A small 1x1 green transparent PNG in base64
mock_base64 = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="

# Generate ID in the format 'SF-YYYYMMDD-HHMMSS' dynamically
time.sleep(1) # Ensure distinct timestamp from any other sequential tests
current_time = datetime.now()
job_id = current_time.strftime("SF-%Y%m%d-%H%M%S")
created_at_str = current_time.strftime("%Y-%m-%d %H:%M:%S")

payload = {
    "action": "create",
    "token": token,
    "imageFolderId": "12FzCcoLz2w7ETwHwFuL4h278vkbKd0WB",
    "data": {
        "id": job_id,
        "area": "A",
        "reporter": "Test Runner",
        "assignee": "สมชาย วงษา",
        "issue": "ปัญหาทดสอบระบบนำเข้า",
        "suggestion": "แก้ไขให้ถูกต้อง",
        "taskType": "safety",
        "status": "pending",
        "photoBefore": mock_base64,
        "createdAt": created_at_str
    }
}

print(f"Creating job with ID: {job_id}...")
try:
    response = requests.post(url, json=payload)
    assert response.status_code == 200, f"Create job failed with status code {response.status_code}"
    resp_json = response.json()
    print("Response text:", response.text)
    assert resp_json.get("status") == "success", f"Failed to create job: {resp_json.get('message')}"
    
    created_id = resp_json.get("id") or resp_json.get("data", {}).get("id")
    assert created_id == job_id, f"Expected created ID to be {job_id}, got {created_id}"
    print("Job successfully created!")
except Exception as e:
    print("Error during job creation:", e)
    raise e

# Clean up the created test job
cleanup_payload = {
    "action": "delete",
    "token": token,
    "data": {
        "id": job_id
    }
}

print(f"Cleaning up test job '{job_id}'...")
response_del = requests.post(url, json=cleanup_payload)
assert response_del.status_code == 200, f"Delete failed with status code {response_del.status_code}"
del_json = response_del.json()
print(f"Cleanup Response: {del_json}")
assert del_json.get("status") == "success", f"Failed to delete test job: {del_json.get('message')}"
print("Cleanup complete!")
