"""
autopilot/notify_owner.py: email the owner the run's "Message for you" (user decision 2026-10-05).

    python -m autopilot.notify_owner --subject "Daily Digest 2026-10-06 · OK" --file message.txt --doc <Doc URL>
    python -m autopilot.notify_owner --subject "…" --file message.txt --dry-run     # prints, sends nothing

Safety:
  - The recipient is FIXED to the owner (OWNER below). There is no option to send anywhere else.
  - Sends from BIZ_MAIL_ADDRESS with BIZ_MAIL_PASSWORD (environment / .env; never printed). Never reads mail.
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
    addr, pw = os.getenv("BIZ_MAIL_ADDRESS", "").strip(), os.getenv("BIZ_MAIL_PASSWORD", "")
    if not (addr and pw):
        sys.exit("NOT SENT: BIZ_MAIL_ADDRESS / BIZ_MAIL_PASSWORD are not set in this environment.")
    return addr, pw


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


def main():
    ap = argparse.ArgumentParser(description="Email the owner the run's message (fixed recipient).")
    ap.add_argument("--subject", required=True)
    ap.add_argument("--file", required=True, help="text file with the 'Message for you'")
    ap.add_argument("--doc", help="link to the full Google Doc")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    body = Path(a.file).read_text(encoding="utf-8")
    if not body.strip():
        sys.exit("NOT SENT: the message file is empty.")
    sender = os.getenv("BIZ_MAIL_ADDRESS", "").strip() or "robot@example.invalid"
    if a.dry_run:
        print(build(sender, a.subject, body, a.doc))
        print("DRY RUN: nothing sent.")
        return
    sender, pw = creds()
    msg = build(sender, a.subject, body, a.doc)
    try:
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=ssl.create_default_context(), timeout=60) as s:
            s.login(sender, pw)
            s.send_message(msg)
    except Exception as e:
        sys.exit("NOT SENT: " + str(e).replace(pw, "[REDACTED]"))
    print(f"✅ Update emailed to {OWNER}: {msg['Subject']}")


if __name__ == "__main__":
    main()
