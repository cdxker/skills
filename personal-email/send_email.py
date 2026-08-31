#!/usr/bin/env python3
"""Send a plaintext email via the SMTP_* env vars (Fastmail).

Usage: send_email.py "Subject" /path/to/body.txt [to-addr]
Default recipient: me@cdxker.com. Always CCs me@cdxker.com when it is not already the recipient.

Sends a single text/plain part, no HTML alternative. Unicode punctuation is
normalized to ASCII so the part can go out 7bit (not base64) — this keeps the
message as plain as email gets and copy/paste-safe in picky clients.
"""
import os
import re
import smtplib
import sys
from email.message import EmailMessage
from pathlib import Path

ASCII_MAP = {
    "—": "--", "–": "-", "‘": "'", "’": "'",
    "“": '"', "”": '"', "…": "...", " ": " ",
    "•": "*", "→": "->",
}

def asciify(text: str) -> str:
    for k, v in ASCII_MAP.items():
        text = text.replace(k, v)
    return text


def header_value(text: str) -> str:
    """Unfold a header and prevent CRLF injection by returning one physical line."""
    return re.sub(r"\s+", " ", asciify(text)).strip()


def build_message(subject: str, body: str, to_addr: str, env=os.environ) -> EmailMessage:
    msg = EmailMessage()
    msg["Subject"] = header_value(subject)
    msg["From"] = header_value(env.get("EMAIL_FROM") or env["SMTP_FROM"])
    msg["To"] = header_value(to_addr)
    if env.get("EMAIL_REPLY_TO"):
        msg["Reply-To"] = header_value(env["EMAIL_REPLY_TO"])
    if env.get("EMAIL_IN_REPLY_TO"):
        in_reply_to = header_value(env["EMAIL_IN_REPLY_TO"])
        references = header_value(env.get("EMAIL_REFERENCES", "") + " " + in_reply_to)
        msg["In-Reply-To"] = in_reply_to
        msg["References"] = references
    cc_addr = "me@cdxker.com"
    if to_addr.strip().lower() != cc_addr:
        msg["Cc"] = cc_addr
    try:
        body.encode("ascii")
        msg.set_content(body, subtype="plain", cte="7bit")
    except UnicodeEncodeError:
        msg.set_content(body, subtype="plain", charset="utf-8", cte="quoted-printable")
    return msg


def main() -> None:
    subject = sys.argv[1]
    body_path = Path(sys.argv[2])
    to_addr = sys.argv[3] if len(sys.argv) > 3 else "me@cdxker.com"
    body = asciify(body_path.read_text())
    msg = build_message(subject, body, to_addr)

    with smtplib.SMTP_SSL(os.environ["SMTP_HOST"], int(os.environ["SMTP_PORT"])) as smtp:
        smtp.login(os.environ["SMTP_USER"], os.environ["SMTP_PASSWORD"])
        smtp.send_message(msg)
    if os.environ.get("EMAIL_SAVE_RAW"):
        Path(os.environ["EMAIL_SAVE_RAW"]).write_bytes(msg.as_bytes())
    print(f"sent to {to_addr} ({msg.get('Content-Transfer-Encoding')}, {msg.get_content_type()})")


if __name__ == "__main__":
    main()
