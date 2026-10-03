"""
make_cloud_env.py: build the COMPLETE text for the Claude cloud environment form and copy it to the clipboard.

    python make_cloud_env.py

What it does (nothing is printed to the screen except names and ✅/❌):
  - takes WP_USERNAME, BING_WMT_API_KEY, DATAFORSEO_LOGIN, DATAFORSEO_PASSWORD from your .env
  - takes the newest Google key file from your Downloads folder
  - asks you to paste the NEW WordPress "robot" password (hidden while you paste)
  - copies all 9 lines, ready to paste into the empty "Environment variables" box
"""

import getpass
import json
import os
import re
import subprocess
import sys
from pathlib import Path


def read_env(path):
    values = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if "=" in line and not line.strip().startswith("#"):
            k, _, v = line.partition("=")
            values[k.strip()] = v.strip().strip('"').strip("'")
    return values


def newest_google_key():
    found = []
    for f in (Path.home() / "Downloads").glob("*.json"):
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
        except (ValueError, OSError):
            continue
        if isinstance(data, dict) and data.get("type") == "service_account" and "private_key" in data:
            found.append((f.stat().st_mtime, f, data))
    return max(found, key=lambda x: x[0]) if found else None


def main():
    env_file = Path(".env")
    if not env_file.is_file():
        sys.exit("❌ I can't find your .env file. First type:  cd C:\\Users\\User\\Documents\\saas  then run this again.")
    env = read_env(env_file)

    key = newest_google_key()
    if not key:
        sys.exit("❌ No Google key file in Downloads. In Google Cloud: gsc-reader → Keys → Add key → Create new key → JSON → Create. Then run this again.")
    _, key_path, key_data = key

    wp_password = ""
    if not os.environ.get("TPG_NO_CLIP"):
        copied = subprocess.run(["powershell", "-NoProfile", "-Command", "Get-Clipboard"],
                                capture_output=True, text=True).stdout.strip()
        if re.fullmatch(r"([A-Za-z0-9]{4} ){5}[A-Za-z0-9]{4}", copied):
            wp_password = copied
            print("✅ Found the WordPress password you copied.")
    if not wp_password:
        print("I didn't find a copied WordPress password.")
        print("Paste it here: right-click once inside this window (you won't see it), then press Enter.")
        wp_password = (getpass.getpass("WordPress robot password: ") if sys.stdin.isatty() else input()).strip()

    lines = {
        "WP_SITE_URL": "https://toolpickguide.com",
        "WP_USERNAME": env.get("WP_USERNAME", ""),
        "WP_APPLICATION_PASSWORD": wp_password,
        "GA4_PROPERTY_ID": "551985779",
        "BING_WMT_API_KEY": env.get("BING_WMT_API_KEY", ""),
        "DATAFORSEO_LOGIN": env.get("DATAFORSEO_LOGIN", ""),
        "DATAFORSEO_PASSWORD": env.get("DATAFORSEO_PASSWORD", ""),
        "TPG_AUTOPILOT": "1",
        "GSC_KEY_JSON": json.dumps(key_data, separators=(",", ":")),
    }
    text = "\n".join(f"{k}={v}" for k, v in lines.items())

    if os.environ.get("TPG_NO_CLIP"):  # test mode: don't touch the clipboard
        print(f"[test] {len(text.splitlines())} lines built")
    else:
        subprocess.run(["clip"], input=text.encode("utf-8"), check=True)

    print("\nChecking the 9 lines:")
    missing = [k for k, v in lines.items() if not v]
    for k, v in lines.items():
        print(f"  {'✅' if v else '❌ EMPTY'}  {k}")
    if missing:
        print(f"\n⚠️  Empty: {', '.join(missing)}. Tell the agent which ones are empty (names only, never values).")
    else:
        print("\n✅ All 9 lines are copied. Now: click the EMPTY Environment variables box and press Ctrl+V. Then Save.")

    answer = input("\nAfter you pasted and saved the form, type  y  and press Enter to delete the downloaded key file: ")
    if answer.strip().lower() == "y":
        key_path.unlink()
        print("🗑️  Deleted the downloaded key file.")


if __name__ == "__main__":
    main()
