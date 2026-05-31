with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Search for pin, pinHash, or sha256 in index.html
for i, line in enumerate(content.splitlines(), 1):
    if "sha256" in line.lower() or "pin" in line.lower() or "crypto" in line.lower():
        print(f"Line {i}: {line.strip()}")
