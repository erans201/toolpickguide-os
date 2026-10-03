"""
make_cloud_key.py: copy the new Google key (from your Downloads folder) to the clipboard as ONE line,
ready to paste after GSC_KEY_JSON= in the Claude cloud environment form.

    python make_cloud_key.py

It never prints the key. It looks for the newest Google service-account .json file in Downloads.
"""

import json
import subprocess
import sys
from pathlib import Path

downloads = Path.home() / "Downloads"
candidates = []
for f in downloads.glob("*.json"):
    try:
        data = json.loads(f.read_text(encoding="utf-8"))
    except (ValueError, OSError):
        continue
    if isinstance(data, dict) and data.get("type") == "service_account" and "private_key" in data:
        candidates.append((f.stat().st_mtime, f, data))

if not candidates:
    sys.exit("❌ No Google key file found in Downloads.\n"
             "   Go back to Google Cloud → gsc-reader → Keys → Add key → Create new key → JSON → Create, then run this again.")

_, path, data = max(candidates, key=lambda c: c[0])
one_line = json.dumps(data, separators=(",", ":"))
subprocess.run(["clip"], input=one_line.encode("utf-8"), check=True)

print(f"✅ Copied! (from the file: {path.name})")
print("   Now go to the Claude form, click right after  GSC_KEY_JSON=  and press Ctrl+V.")
answer = input("\nAfter you have pasted it and saved the form, type  y  and press Enter to delete the downloaded key file (or just press Enter to keep it): ")
if answer.strip().lower() == "y":
    path.unlink()
    print("🗑️  Deleted the downloaded key file.")
