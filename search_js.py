import re

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Search for fetch calls
fetch_blocks = re.findall(r"fetch\(.*?\)", content, re.DOTALL)
print("Fetch calls found in index.html:")
for block in fetch_blocks:
    print(block.strip())
    print("-" * 30)

# Search for script methods
print("\nSearching for GET/POST methods or payload structures:")
for line in content.splitlines():
    if "action:" in line or "method:" in line or "payload" in line:
        print(line.strip())
