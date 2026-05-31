import requests

sheet_url = "https://docs.google.com/spreadsheets/d/18fG-3MpRqiDe2EjJcdqqG_i6BdCEYFjdUqS4uYi6F3k/export?format=xlsx"

try:
    response = requests.get(sheet_url)
    print("Download Status:", response.status_code)
    if response.status_code == 200:
        with open("live_database.xlsx", "wb") as f:
            f.write(response.content)
        print("Spreadsheet downloaded successfully as live_database.xlsx!")
    else:
        print("Failed to download. Response text length:", len(response.text))
except Exception as e:
    print("Error:", e)
