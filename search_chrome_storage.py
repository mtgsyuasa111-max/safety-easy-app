import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

chrome_dir = r"C:\Users\db2b2\AppData\Local\Google\Chrome\User Data"
print("Scanning Chrome profiles for LevelDB storage...")

# Find all LevelDB directories
leveldb_dirs = []
for root, dirs, files in os.walk(chrome_dir):
    if "Local Storage" in root and root.endswith("leveldb"):
        leveldb_dirs.append(root)

print(f"Found {len(leveldb_dirs)} LevelDB directories.")

keywords = [b"safety_easy", b"safety_users", b"auth_token", b"AUTH_", b"vercel"]

for ldb in leveldb_dirs:
    print(f"\nScanning: {ldb}")
    for file in os.listdir(ldb):
        if file.endswith((".log", ".ldb", ".sst")):
            path = os.path.join(ldb, file)
            try:
                with open(path, "rb") as f:
                    content = f.read()
                for kw in keywords:
                    if kw in content:
                        print(f"  MATCH in {file} for keyword {kw.decode('utf-8')}")
                        # Print some surrounding context
                        idx = content.index(kw)
                        start = max(0, idx - 100)
                        end = min(len(content), idx + 200)
                        context = content[start:end]
                        print("  Context:")
                        # Clean up non-printable bytes
                        clean_context = "".join(chr(b) if 32 <= b < 127 or b == 10 or b == 13 else "." for b in context)
                        print(f"    {clean_context}")
            except Exception as e:
                print(f"  Error reading {file}: {e}")
