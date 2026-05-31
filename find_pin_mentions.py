import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("Searching for PIN mentions...")

keywords = ["pin", "รหัส", "password", "hash"]
for root, dirs, files in os.walk(r"d:\D2B"):
    if ".git" in root or ".vercel" in root or "chrome-profile" in root:
        continue
    for file in files:
        if file.endswith((".js", ".html", ".txt", ".md", ".gs")):
            path = os.path.join(root, file)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                for i, line in enumerate(content.splitlines(), 1):
                    if any(k in line.lower() for k in keywords):
                        if any(num in line for num in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]):
                            # Print matching line
                            if len(line.strip()) < 120:
                                print(f"{file}:{i} -> {line.strip()}")
            except Exception:
                pass
