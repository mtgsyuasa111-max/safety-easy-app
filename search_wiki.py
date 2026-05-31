import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

wiki_dir = r"D:\oat\wiki\gemini-obsidian\wiki"
print("Scanning wiki directory for PINs and credentials...")

keywords = ["pin", "รหัส", "password", "hash"]
found = False

for root, dirs, files in os.walk(wiki_dir):
    for file in files:
        if file.endswith(".md"):
            path = os.path.join(root, file)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                for i, line in enumerate(content.splitlines(), 1):
                    if any(k in line.lower() for k in keywords):
                        # Show match
                        print(f"{file}:{i} -> {line.strip()[:150]}")
                        found = True
            except Exception as e:
                pass

if not found:
    print("No mentions found in wiki.")
