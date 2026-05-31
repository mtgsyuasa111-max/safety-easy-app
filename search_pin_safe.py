import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Search for pin, pinHash, or sha256 in index.html
for i, line in enumerate(content.splitlines(), 1):
    lower_line = line.lower()
    if "sha256" in lower_line or "pin" in lower_line or "crypto" in lower_line or "hash" in lower_line:
        print(f"Line {i}: {line.strip()}")
