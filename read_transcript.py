import os
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

log_dir = r"C:\Users\db2b2\.gemini\antigravity\brain\d58a53eb-43f7-43a2-939e-0dfc0b09ed62\.system_generated\logs"
transcript_path = os.path.join(log_dir, "transcript.jsonl")

print("Transcript path:", transcript_path)
if not os.path.exists(transcript_path):
    print("Transcript file does not exist!")
    sys.exit(0)

print("Searching transcript for PIN or login details...")
with open(transcript_path, "r", encoding="utf-8") as f:
    for line_num, line in enumerate(f, 1):
        try:
            step = json.loads(line)
            content = step.get("content", "")
            if not content:
                # Check tool calls or other fields
                content = json.dumps(step)
            
            # Look for keywords
            keywords = ["pin", "รหัส", "password", "hash"]
            if any(k in content.lower() for k in keywords):
                # Print index, source, type, and snippet
                print(f"Line {line_num} (Step {step.get('step_index')}, Source: {step.get('source')}):")
                # Snippet of content
                for word in keywords:
                    idx = content.lower().find(word)
                    if idx != -1:
                        start = max(0, idx - 80)
                        end = min(len(content), idx + 80)
                        print(f"  Snippet for '{word}': ...{content[start:end]}...")
        except Exception as e:
            print(f"Error parsing line {line_num}: {e}")
