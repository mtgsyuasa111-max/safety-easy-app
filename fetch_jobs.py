import requests
import json

url = "https://script.google.com/macros/s/AKfycbzHtI57K9rvIFtS3FCUCkuuiLiHClyimHy5OjM6uCWHvCqpSrnIe6NYR18LyurTOFPi_w/exec"

for action in ["getJobs", "get_jobs", "jobs", "read"]:
    try:
        response = requests.get(url, params={"action": action})
        print(f"Action {action} Status code:", response.status_code)
        data = response.json()
        print(f"Action {action} Response:", json.dumps(data, indent=2, ensure_ascii=False)[:300])
    except Exception as e:
        print(f"Action {action} Error:", e)
