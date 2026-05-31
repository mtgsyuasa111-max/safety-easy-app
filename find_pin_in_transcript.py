import os
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

log_dir = r"C:\Users\db2b2\.gemini\antigravity\brain\d58a53eb-43f7-43a2-939e-0dfc0b09ed62\.system_generated\logs"
transcript_path = os.path.join(log_dir, "transcript.jsonl")

if not os.path.exists(transcript_path):
    print("Transcript does not exist!")
    sys.exit(0)

print("Scanning full transcript text...")

with open(transcript_path, "r", encoding="utf-8") as f:
    for line_num, line in enumerate(f, 1):
        # Scan the raw line as a string
        line_lower = line.lower()
        if "รหัส" in line_lower or "pin" in line_lower:
            try:
                step = json.loads(line)
                step_idx = step.get("step_index")
                source = step.get("source")
                stype = step.get("type")
                
                # Check if it contains actual disclosures like "PIN is" or "รหัสคือ"
                # Or just print some lines from early steps (e.g. step_idx < 100) where the PIN request was processed
                if step_idx < 300:
                    # Print snippet of the raw line
                    snippet = line.strip()[:200]
                    print(f"Line {line_num} (Step {step_idx}, Type: {stype}, Source: {source}):")
                    print(f"  Snippet: {snippet}...")
            except Exception as e:
                pass

print("Scan complete.")
