import os
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

log_dir = r"C:\Users\db2b2\.gemini\antigravity\brain\d58a53eb-43f7-43a2-939e-0dfc0b09ed62\.system_generated\logs"
transcript_path = os.path.join(log_dir, "transcript.jsonl")

if not os.path.exists(transcript_path):
    print("Transcript does not exist!")
    sys.exit(0)

# Read total lines
with open(transcript_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

print("Total steps in transcript:", len(lines))

# Print step indices for first 5 steps and last 5 steps
for i in list(range(5)) + list(range(len(lines)-5, len(lines))):
    if 0 <= i < len(lines):
        try:
            step = json.loads(lines[i])
            print(f"Index {i} -> Step Index: {step.get('step_index')}, Type: {step.get('type')}, Source: {step.get('source')}")
        except Exception as e:
            print(f"Index {i} -> Error: {e}")
