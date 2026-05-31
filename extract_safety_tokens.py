import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

profiles = [
    r"C:\Users\db2b2\AppData\Local\Google\Chrome\User Data\Profile 5\Local Storage\leveldb",
    r"C:\Users\db2b2\AppData\Local\Google\Chrome\User Data\Profile 6\Local Storage\leveldb",
    r"C:\Users\db2b2\AppData\Local\Google\Chrome\User Data\Profile 1\Local Storage\leveldb",
    r"C:\Users\db2b2\AppData\Local\Google\Chrome\User Data\Default\Local Storage\leveldb"
]

print("Scanning for safety-easy-app local storage and session tokens...")

# Look for auth token pattern (AUTH_ followed by uuid or alphanumeric)
# Look for PIN strings (4 digits) next to user names
token_pattern = re.compile(b"AUTH_[a-zA-Z0-9_-]+")

for p_dir in profiles:
    if not os.path.exists(p_dir):
        continue
    print(f"\nScanning Profile Dir: {p_dir}")
    for file in os.listdir(p_dir):
        if file.endswith((".log", ".ldb", ".sst")):
            path = os.path.join(p_dir, file)
            try:
                with open(path, "rb") as f:
                    content = f.read()
                
                # Check for tokens
                tokens = token_pattern.findall(content)
                if tokens:
                    for t in set(tokens):
                        print(f"  [TOKEN FOUND] in {file}: {t.decode('utf-8')}")
                
                # Check for vercel storage values
                if b"safety_" in content or b"safety-easy-app" in content:
                    print(f"  [SAFETY KEYWORDS FOUND] in {file}")
                    # Try to extract JSON strings
                    json_matches = re.findall(b"\\{[^{}]*?\"[a-zA-Z0-9_-]*?\"[^{}]*?\\}", content)
                    for jm in json_matches:
                        if b"U00" in jm or b"admin" in jm or b"supervisor" in jm:
                            try:
                                # Clean up non-printable bytes
                                s = jm.decode('utf-8', errors='ignore')
                                # Print if it looks like a user JSON
                                if "role" in s and "name" in s:
                                    print(f"    User JSON snippet: {s}")
                            except Exception:
                                pass
            except Exception as e:
                print(f"  Error reading {file}: {e}")

print("\nScan completed!")
