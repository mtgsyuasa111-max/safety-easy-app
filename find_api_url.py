import re

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Search for lines containing script.google.com or similar
for i, line in enumerate(content.splitlines(), 1):
    if "script.google.com" in line or "18fG-3MpRqiDe2EjJcdqqG_i6BdCEYFjdUqS4uYi6F3k" in line or "API_URL" in line:
        print(f"Line {i}: {line.strip()}")
