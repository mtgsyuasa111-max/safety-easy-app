import os
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

log_dir = r"C:\Users\db2b2\.gemini\antigravity\brain\d58a53eb-43f7-43a2-939e-0dfc0b09ed62\.system_generated\logs"
transcript_path = os.path.join(log_dir, "transcript.jsonl")

if not os.path.exists(transcript_path):
    print("Transcript does not exist!")
    sys.exit(0)

print("Scanning full transcript steps for PIN answers...")

with open(transcript_path, "r", encoding="utf-8") as f:
    for line_num, line in enumerate(f, 1):
        try:
            step = json.loads(line)
            stype = step.get("type")
            source = step.get("source")
            content = step.get("content", "")
            
            if stype in ["USER_INPUT", "PLANNER_RESPONSE"] and content:
                content_lower = content.lower()
                if "รหัส" in content_lower or "pin" in content_lower:
                    # Let's print the entire content if it is short, or search for numbers
                    # Print step information
                    print(f"\n==================================================")
                    print(f"Line {line_num} | Step {step.get('step_index')} | Type: {stype} | Source: {source}")
                    print(f"==================================================")
                    print(content)
        except Exception as e:
            pass

print("\nScan complete.")
