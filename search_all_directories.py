import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("Searching all files in d:\\D2B excluding node_modules...")
keywords = ["u001", "u002", "u003", "4efba02990e4356fb31c65e1637a7162ccc4449870a4c26ccab052ffecae9d42"]
found = False

for root, dirs, files in os.walk(r"d:\D2B"):
    # Skip standard directories to prevent lock issues and speed up
    if "node_modules" in root or "chrome-profile" in root or ".git" in root or ".pnpm" in root:
        continue
    for file in files:
        if file.endswith((".js", ".html", ".txt", ".md", ".json", ".gs")):
            path = os.path.join(root, file)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                for i, line in enumerate(content.splitlines(), 1):
                    if any(k in line.lower() for k in keywords):
                        # Skip if it is our search scripts or output files
                        if any(s in file for s in ["search", "crack", "inspect", "detailed", "fetch", "read_transcript", "test_"]):
                            continue
                        print(f"{path}:{i} -> {line.strip()[:150]}")
                        found = True
            except Exception:
                pass

if not found:
    print("No mentions found.")
