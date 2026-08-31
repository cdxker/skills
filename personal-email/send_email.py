#!/usr/bin/env python3
"""Send a plaintext email via the SMTP_* env vars (Fastmail).

Usage: send_email.py "Subject" /path/to/body.txt [to-addr]
Default recipient: me@cdxker.com. Always CCs me@cdxker.com when it is not already the recipient.

Sends a single text/plain part, no HTML alternative. Unicode punctuation is
normalized to ASCII so the part can go out 7bit (not base64) — this keeps the
message as plain as email gets and copy/paste-safe in picky clients.
"""
import os
import smtplib
import sys
from email.message import EmailMessage

ASCII_MAP = {
    "—": "--", "–": "-", "‘": "'", "’": "'",
    "“": '"', "”": '"', "…": "...", " ": " ",
    "•": "*", "→": "->",
}

def asciify(text: str) -> str:
    for k, v in ASCII_MAP.items():
        text = text.replace(k, v)
    return text

subject = sys.argv[1]
body_path = sys.argv[2]
to_addr = sys.argv[3] if len(sys.argv) > 3 else "me@cdxker.com"

body = asciify(open(body_path).read())

msg = EmailMessage()
msg["Subject"] = asciify(subject)
msg["From"] = os.environ.get("EMAIL_FROM") or os.environ["SMTP_FROM"]
msg["To"] = to_addr
if os.environ.get("EMAIL_REPLY_TO"):
    msg["Reply-To"] = os.environ["EMAIL_REPLY_TO"]
if os.environ.get("EMAIL_IN_REPLY_TO"):  # thread this message under an existing one
    msg["In-Reply-To"] = os.environ["EMAIL_IN_REPLY_TO"]
    msg["References"] = (os.environ.get("EMAIL_REFERENCES", "") + " " + os.environ["EMAIL_IN_REPLY_TO"]).strip()
CC_ADDR = "me@cdxker.com"
if to_addr.strip().lower() != CC_ADDR:
    msg["Cc"] = CC_ADDR
try:
    body.encode("ascii")
    msg.set_content(body, subtype="plain", cte="7bit")
except UnicodeEncodeError:
    msg.set_content(body, subtype="plain", charset="utf-8", cte="quoted-printable")

with smtplib.SMTP_SSL(os.environ["SMTP_HOST"], int(os.environ["SMTP_PORT"])) as s:
    s.login(os.environ["SMTP_USER"], os.environ["SMTP_PASSWORD"])
    s.send_message(msg)
if os.environ.get("EMAIL_SAVE_RAW"):  # let callers file a copy of exactly what went out (run.py appends it to <Role>/In)
    open(os.environ["EMAIL_SAVE_RAW"], "wb").write(msg.as_bytes())
print(f"sent to {to_addr} ({msg.get('Content-Transfer-Encoding')}, {msg.get_content_type()})")
