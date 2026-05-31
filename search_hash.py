import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Search for digest, sha, crypto, hex, or hashing
for i, line in enumerate(content.splitlines(), 1):
    lower_line = line.lower()
    if any(k in lower_line for k in ["digest", "crypto", "subtle", "hex", "encode", "hash"]):
        if len(line.strip()) < 150:
            print(f"Line {i}: {line.strip()}")
        else:
            print(f"Line {i}: {line.strip()[:150]}...")
