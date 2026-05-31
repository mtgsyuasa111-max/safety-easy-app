import os
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

log_dir = r"C:\Users\db2b2\.gemini\antigravity\brain\d58a53eb-43f7-43a2-939e-0dfc0b09ed62\.system_generated\logs"
transcript_path = os.path.join(log_dir, "transcript.jsonl")

if not os.path.exists(transcript_path):
    print("Transcript does not exist!")
    sys.exit(0)

print("Scanning steps around token message...")

with open(transcript_path, "r", encoding="utf-8") as f:
    for line_num, line in enumerate(f, 1):
        try:
            step = json.loads(line)
            step_idx = step.get("step_index")
            source = step.get("source")
            stype = step.get("type")
            content = step.get("content", "")
            
            if 820 <= step_idx <= 860 and content:
                print(f"\n==================================================")
                print(f"Line {line_num} | Step {step_idx} | Type: {stype} | Source: {source}")
                print(f"==================================================")
                print(content)
        except Exception:
            pass

print("Scan complete.")
