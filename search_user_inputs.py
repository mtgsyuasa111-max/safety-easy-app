import os
import json
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

log_dir = r"C:\Users\db2b2\.gemini\antigravity\brain\d58a53eb-43f7-43a2-939e-0dfc0b09ed62\.system_generated\logs"
transcript_path = os.path.join(log_dir, "transcript.jsonl")

if not os.path.exists(transcript_path):
    print("Transcript does not exist!")
    sys.exit(0)

print("Scanning user messages for 4-digit PINs...")
with open(transcript_path, "r", encoding="utf-8") as f:
    for line_num, line in enumerate(f, 1):
        try:
            step = json.loads(line)
            stype = step.get("type")
            source = step.get("source")
            content = step.get("content", "")
            
            if stype == "USER_INPUT" and content:
                # Find all 4-digit numbers
                pins = re.findall(r"\b\d{4}\b", content)
                if pins:
                    print(f"Line {line_num} (Step {step.get('step_index')}):")
                    print(f"  User message: {content.strip()}")
                    print(f"  Found potential PINs: {pins}")
        except Exception:
            pass

print("Scan complete.")
