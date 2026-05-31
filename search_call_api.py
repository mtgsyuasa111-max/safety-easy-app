import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("index.html", "r", encoding="utf-8") as f:
    lines = f.splitlines() if hasattr(f, 'splitlines') else f.read().splitlines()

for i, line in enumerate(lines, 1):
    if "async function callApi" in line or "function callApi" in line:
        for j in range(i-1, min(i+80, len(lines))):
            print(f"Line {j+1}: {lines[j]}")
        break
