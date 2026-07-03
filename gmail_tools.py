"""
gmail_tools.py
--------------
Four LangChain @tool-decorated functions that wrap the Gmail API.

Tools available:
  - list_emails(query)        : List emails matching a query (default: inbox)
  - read_email(message_id)    : Read full content of a single email
  - send_email(json_str)      : Send a new email (JSON: to, subject, body)
  - delete_email(message_id)  : Permanently delete an email (NOT trash)
"""

import base64
import json
from email.mime.text import MIMEText

from langchain_core.tools import tool

from gmail_auth import get_gmail_service


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def _get_header(headers: list, name: str) -> str:
    """Extract a specific header value from a list of Gmail header dicts."""
    for h in headers:
        if h.get("name", "").lower() == name.lower():
            return h.get("value", "")
    return ""


def _decode_body(payload: dict) -> str:
    """
    Recursively extract and base64-decode the plain-text body from a Gmail
    message payload (handles both simple and multipart messages).
    """
    mime_type = payload.get("mimeType", "")

    # Simple (non-multipart) message
    if "parts" not in payload:
        data = payload.get("body", {}).get("data", "")
        if data:
            return base64.urlsafe_b64decode(data).decode("utf-8", errors="replace")
        return ""

    # Multipart: prefer text/plain, fall back to first part
    for part in payload["parts"]:
        if part.get("mimeType") == "text/plain":
            data = part.get("body", {}).get("data", "")
            if data:
                return base64.urlsafe_b64decode(data).decode("utf-8", errors="replace")

    # Recurse into nested multipart
    for part in payload["parts"]:
        result = _decode_body(part)
        if result:
            return result

    return ""


# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------

@tool
def list_emails(query: str) -> str:
    """
    List emails from Gmail matching the given query.

    Args:
        query: Gmail search query string, e.g. 'in:inbox', 'is:unread',
               'from:boss@company.com', or 'in:inbox' for latest inbox emails.
               Pass 'in:inbox' to list the most recent inbox emails.

    Returns:
        A formatted string listing each email's index, sender, subject, and date.
    """
    service = get_gmail_service()

    result = service.users().messages().list(
        userId="me",
        q=query,
        maxResults=10
    ).execute()

    messages = result.get("messages", [])
    if not messages:
        return "No emails found matching the query."

    lines = [f"Found {len(messages)} email(s):\n"]
    for i, msg_ref in enumerate(messages, start=1):
        msg = service.users().messages().get(
            userId="me",
            id=msg_ref["id"],
            format="metadata",
            metadataHeaders=["From", "Subject", "Date"]
        ).execute()

        headers = msg.get("payload", {}).get("headers", [])
        sender  = _get_header(headers, "From")
        subject = _get_header(headers, "Subject")
        date    = _get_header(headers, "Date")

        lines.append(
            f"{i}. ID: {msg_ref['id']}\n"
            f"   From:    {sender}\n"
            f"   Subject: {subject}\n"
            f"   Date:    {date}\n"
        )

    return "\n".join(lines)


@tool
def read_email(message_id: str) -> str:
    """
    Read the full content of a single Gmail email by its message ID.

    Args:
        message_id: The Gmail message ID (e.g. obtained from list_emails).

    Returns:
        A formatted string with the email's sender, subject, date, and body.
    """
    service = get_gmail_service()

    msg = service.users().messages().get(
        userId="me",
        id=message_id,
        format="full"
    ).execute()

    headers = msg.get("payload", {}).get("headers", [])
    sender  = _get_header(headers, "From")
    subject = _get_header(headers, "Subject")
    date    = _get_header(headers, "Date")
    body    = _decode_body(msg.get("payload", {}))

    return (
        f"From:    {sender}\n"
        f"Subject: {subject}\n"
        f"Date:    {date}\n"
        f"{'─' * 50}\n"
        f"{body.strip() if body else '[No plain-text body found]'}"
    )


@tool
def send_email(to_subject_body: str) -> str:
    """
    Send a new email via Gmail.

    Args:
        to_subject_body: A JSON string with keys 'to', 'subject', and 'body'.
            Example: '{"to": "alice@example.com", "subject": "Hello", "body": "Hi Alice!"}'

    Returns:
        A confirmation string with the sent message ID, or an error description.
    """
    try:
        data = json.loads(to_subject_body)
        to      = data["to"]
        subject = data["subject"]
        body    = data["body"]
    except (json.JSONDecodeError, KeyError) as exc:
        return (
            f"Invalid input. Provide a JSON string with keys 'to', 'subject', 'body'. "
            f"Error: {exc}"
        )

    # Build a MIME message
    mime_message = MIMEText(body)
    mime_message["to"]      = to
    mime_message["subject"] = subject

    # Base64url-encode the raw MIME bytes
    raw = base64.urlsafe_b64encode(mime_message.as_bytes()).decode("utf-8")

    service = get_gmail_service()
    sent = service.users().messages().send(
        userId="me",
        body={"raw": raw}
    ).execute()

    return f"Email sent successfully. Message ID: {sent['id']}"


@tool
def delete_email(message_id: str) -> str:
    """
    Permanently delete a Gmail email by its message ID.
    WARNING: This action is irreversible — the email is NOT moved to Trash.

    Args:
        message_id: The Gmail message ID to permanently delete.

    Returns:
        A confirmation string.
    """
    service = get_gmail_service()

    # users.messages.delete permanently removes the message
    service.users().messages().delete(
        userId="me",
        id=message_id
    ).execute()

    return f"Email {message_id} has been permanently deleted."


# ---------------------------------------------------------------------------
# Tool registry
# ---------------------------------------------------------------------------

def get_tools() -> list:
    """Return all Gmail tools for use with the LangChain agent."""
    return [list_emails, read_email, send_email, delete_email]
