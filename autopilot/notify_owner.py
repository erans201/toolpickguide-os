"""
autopilot/notify_owner.py: email the owner the run's "Message for you" (user decision 2026-10-05).

    python -m autopilot.notify_owner --subject "Daily Digest 2026-10-06 · OK" --file message.txt --doc <Doc URL>
    python -m autopilot.notify_owner --subject "…" --file message.txt --dry-run     # prints, sends nothing

Safety:
  - The recipient is FIXED to the owner (OWNER below). There is no option to send anywhere else.
  - Sends from BIZ_MAIL_ADDRESS with BIZ_MAIL_PASSWORD (environment / .env; never printed). Never reads mail.
  - The cloud sandbox blocks direct mail connections, so --via auto falls back to the website:
    wordpress/toolpickguide-owner-mail.php (mu-plugin, same fixed recipient, 10/day cap) sends it.
  - Plain text only, no attachments. Errors never show the password.
  - Allowed under the cloud autopilot (unlike mail_tool.py), because it can only ever write to the owner.
"""

import argparse
import os
import smtplib
import ssl
import sys
from email.message import EmailMessage
from email.utils import formatdate, make_msgid
from pathlib import Path

OWNER = "cezaris.joe@gmail.com"  # the only recipient (user decision 2026-10-05)
SMTP_HOST, SMTP_PORT = "smtp.hostinger.com", 465
MAX_CHARS = 20000


def creds():
    try:
        from dotenv import load_dotenv
        load_dotenv(Path(__file__).resolve().parent.parent / ".env")
    except ImportError:
        pass
    return os.getenv("BIZ_MAIL_ADDRESS", "").strip(), os.getenv("BIZ_MAIL_PASSWORD", "")


def build(sender, subject, body, doc=None):
    text = body.strip()[:MAX_CHARS]
    if doc:
        text += f"\n\nFull report: {doc}"
    text += "\n\n(Sent automatically by the ToolPickGuide robot. It can only email this address.)"
    msg = EmailMessage()
    msg["From"], msg["To"], msg["Subject"] = f"ToolPickGuide robot <{sender}>", OWNER, subject.strip()[:200]
    msg["Date"], msg["Message-ID"] = formatdate(localtime=True), make_msgid(domain=sender.split("@")[-1])
    msg.set_content(text)
    return msg


def send_smtp(msg):
    sender, pw = creds()
    if not (sender and pw):
        return "smtp: BIZ_MAIL_ADDRESS / BIZ_MAIL_PASSWORD are not set"
    try:
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=ssl.create_default_context(), timeout=30) as s:
            s.login(sender, pw)
            s.send_message(msg)
    except Exception as e:
        return "smtp: " + str(e).replace(pw, "[REDACTED]")
    return None


def send_wp(msg):
    """Fallback for the cloud robot (no direct mail connections there): the site's mu-plugin
    wordpress/toolpickguide-owner-mail.php sends it with wp_mail() to the same fixed owner."""
    import base64
    import requests
    site = os.getenv("WP_SITE_URL", "").rstrip("/")
    user, pw = os.getenv("WP_USERNAME", ""), os.getenv("WP_APPLICATION_PASSWORD", "")
    if not (site.startswith("https://") and user and pw):
        return "website: WP_SITE_URL / WP_USERNAME / WP_APPLICATION_PASSWORD are not set"
    token = base64.b64encode(f"{user}:{pw}".encode()).decode()
    try:
        r = requests.post(f"{site}/wp-json/tpg/v1/notify-owner", timeout=60, auth=(user, pw),
                          headers={"X-WP-Auth": f"Basic {token}", "User-Agent": "ToolPickGuide-Robot/1.0"},
                          json={"subject": msg["Subject"], "body": msg.get_content()})
    except Exception as e:
        return "website: " + str(e).replace(pw, "[REDACTED]").replace(token, "[REDACTED]")
    if r.status_code == 404:
        return "website: the owner-mail plugin is not installed (wordpress/toolpickguide-owner-mail.php)"
    if r.status_code != 200:
        return f"website: HTTP {r.status_code} {r.text[:200]}"
    return None


def main():
    ap = argparse.ArgumentParser(description="Email the owner the run's message (fixed recipient).")
    ap.add_argument("--subject", required=True)
    ap.add_argument("--file", required=True, help="text file with the 'Message for you'")
    ap.add_argument("--doc", help="link to the full Google Doc")
    ap.add_argument("--via", choices=["auto", "smtp", "wp"], default="auto",
                    help="auto = mail server first, then the website if that fails")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    body = Path(a.file).read_text(encoding="utf-8")
    if not body.strip():
        sys.exit("NOT SENT: the message file is empty.")
    try:
        from dotenv import load_dotenv
        load_dotenv(Path(__file__).resolve().parent.parent / ".env")
    except ImportError:
        pass
    sender = os.getenv("BIZ_MAIL_ADDRESS", "").strip() or "eran@toolpickguide.com"
    msg = build(sender, a.subject, body, a.doc)
    if a.dry_run:
        print(msg)
        print("DRY RUN: nothing sent.")
        return
    errors = []
    for way, fn in (("smtp", send_smtp), ("wp", send_wp)):
        if a.via not in ("auto", way):
            continue
        err = fn(msg)
        if not err:
            print(f"✅ Update emailed to {OWNER} ({'mail server' if way == 'smtp' else 'website'}): {msg['Subject']}")
            return
        errors.append(err)
    sys.exit("NOT SENT: " + " | ".join(errors))


if __name__ == "__main__":
    main()
