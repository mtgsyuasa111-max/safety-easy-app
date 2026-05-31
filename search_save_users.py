import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

print("Searching for saveUsers function in index.html...")
lines = content.splitlines()
for i, line in enumerate(lines, 1):
    if "function saveusers" in line.lower() or "saveusers = " in line.lower():
        for j in range(max(0, i-2), min(i+40, len(lines))):
            print(f"Line {j+1}: {lines[j]}")
        break
