import sys

sys.stdout.reconfigure(encoding='utf-8')

path = r"d:\D2B\gas_project\Index.html"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

print("Searching Index.html in gas_project for pin or hash...")
for i, line in enumerate(content.splitlines(), 1):
    if any(k in line.lower() for k in ["pin", "hash", "password", "sha"]):
        print(f"Line {i}: {line.strip()[:150]}")
