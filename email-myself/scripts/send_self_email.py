#!/usr/bin/env python3
"""Send a plain-text email to the user's fixed self-address using SMTP env vars."""

from __future__ import annotations

import argparse
import mimetypes
import os
import smtplib
import ssl
import sys
from email.message import EmailMessage
from pathlib import Path


RECIPIENT = "me@cdxker.com"
REQUIRED_ENV = ("SMTP_HOST", "SMTP_PORT", "SMTP_USER", "SMTP_PASSWORD")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=f"Send an email to {RECIPIENT}")
    parser.add_argument("--subject", required=True, help="Email subject")
    body_group = parser.add_mutually_exclusive_group()
    body_group.add_argument("--body", help="Plain-text body")
    body_group.add_argument("--body-file", type=Path, help="UTF-8 plain-text body file")
    parser.add_argument(
        "--attach",
        action="append",
        type=Path,
        default=[],
        help="File to attach; repeat for multiple files",
    )
    parser.add_argument("--dry-run", action="store_true", help="Validate without sending")
    return parser.parse_args()


def require_config() -> dict[str, str]:
    missing = [name for name in REQUIRED_ENV if not os.environ.get(name)]
    if missing:
        raise ValueError("Missing SMTP configuration: " + ", ".join(missing))
    values = {name: os.environ[name] for name in REQUIRED_ENV}
    values["SMTP_FROM"] = os.environ.get("SMTP_FROM", RECIPIENT)
    values["SMTP_SECURE"] = os.environ.get("SMTP_SECURE", "")
    try:
        port = int(values["SMTP_PORT"])
    except ValueError as exc:
        raise ValueError("SMTP_PORT must be an integer") from exc
    if not 1 <= port <= 65535:
        raise ValueError("SMTP_PORT must be between 1 and 65535")
    return values


def resolve_body(args: argparse.Namespace) -> str:
    if args.body is not None:
        body = args.body
    elif args.body_file is not None:
        try:
            body = args.body_file.read_text(encoding="utf-8")
        except OSError as exc:
            raise ValueError(f"Cannot read body file: {args.body_file}") from exc
    elif not sys.stdin.isatty():
        body = sys.stdin.read()
    else:
        raise ValueError("Provide --body, --body-file, or pipe the message body on stdin")
    if not body.strip():
        raise ValueError("Email body cannot be empty")
    return body


def build_message(args: argparse.Namespace, config: dict[str, str], body: str) -> EmailMessage:
    if "\n" in args.subject or "\r" in args.subject:
        raise ValueError("Subject cannot contain newlines")
    message = EmailMessage()
    message["Subject"] = args.subject
    message["From"] = config["SMTP_FROM"]
    message["To"] = RECIPIENT
    message.set_content(body)

    for attachment in args.attach:
        if not attachment.is_file():
            raise ValueError(f"Attachment is not a readable file: {attachment}")
        mime_type, _ = mimetypes.guess_type(attachment.name)
        maintype, subtype = (mime_type or "application/octet-stream").split("/", 1)
        try:
            payload = attachment.read_bytes()
        except OSError as exc:
            raise ValueError(f"Cannot read attachment: {attachment}") from exc
        message.add_attachment(
            payload,
            maintype=maintype,
            subtype=subtype,
            filename=attachment.name,
        )
    return message


def send(message: EmailMessage, config: dict[str, str]) -> None:
    host = config["SMTP_HOST"]
    port = int(config["SMTP_PORT"])
    secure = config["SMTP_SECURE"].strip().lower()
    implicit_tls = port == 465 or secure in {"1", "true", "yes", "ssl", "smtps", "implicit"}
    context = ssl.create_default_context()

    if implicit_tls:
        with smtplib.SMTP_SSL(host, port, context=context, timeout=30) as smtp:
            smtp.login(config["SMTP_USER"], config["SMTP_PASSWORD"])
            smtp.send_message(message)
        return

    with smtplib.SMTP(host, port, timeout=30) as smtp:
        smtp.ehlo()
        smtp.starttls(context=context)
        smtp.ehlo()
        smtp.login(config["SMTP_USER"], config["SMTP_PASSWORD"])
        smtp.send_message(message)


def main() -> int:
    try:
        args = parse_args()
        config = require_config()
        body = resolve_body(args)
        message = build_message(args, config, body)
        if args.dry_run:
            print(
                f"Dry run valid: To={RECIPIENT}, Subject={args.subject!r}, "
                f"Attachments={len(args.attach)}"
            )
            return 0
        send(message, config)
        print(f"SMTP server accepted email to {RECIPIENT}")
        return 0
    except (ValueError, OSError, smtplib.SMTPException) as exc:
        print(f"Email not sent: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
