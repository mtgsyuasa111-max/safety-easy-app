import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

print("Searching index.html for user saving logic...")
lines = content.splitlines()
for i, line in enumerate(lines, 1):
    if "adduser" in line.lower() or "saveuser" in line.lower() or "pin" in line.lower() and "user" in line.lower() and "action" in line.lower():
        # Print next 5 lines
        for j in range(max(0, i-5), min(i+15, len(lines))):
            print(f"Line {j+1}: {lines[j]}")
        print("-" * 50)
