# ============================================================
# email_sender.py - SMTP Email Sending (Real + Dry-Run)
# Email Automation & Reminder System
# ============================================================

import sys
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Windows UTF-8 fix
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from src.logger import setup_logger

logger = setup_logger()


def send_email(to_email: str, subject: str, body: str, dry_run: bool = None) -> dict:
    """
    Send an email or simulate sending in dry-run mode.
    dry_run parameter takes priority over environment variable.
    """
    # Determine dry_run: explicit param > env var > default True (safe)
    if dry_run is None:
        dry_run = os.environ.get("DRY_RUN", "true").lower() != "false"

    result = {
        "to_email": to_email,
        "subject":  subject,
        "status":   "pending",
        "message":  ""
    }

    if dry_run:
        logger.info(f"[DRY-RUN] SIMULATED -> To: {to_email} | Subject: {subject}")
        print("-" * 60)
        print(f"  [DRY-RUN] EMAIL SIMULATED")
        print(f"  To      : {to_email}")
        print(f"  Subject : {subject}")
        preview = body.strip()[:250].replace("\n", " ")
        print(f"  Preview : {preview}...")
        print("-" * 60)
        print("")
        result["status"]  = "simulated"
        result["message"] = "Dry-run: email not actually sent"
        return result

    # --- REAL SMTP SEND ---
    smtp_host     = os.environ.get("SMTP_HOST", "smtp.gmail.com")
    smtp_port     = int(os.environ.get("SMTP_PORT", 587))
    sender_email  = os.environ.get("SENDER_EMAIL", "")
    sender_pass   = os.environ.get("SENDER_PASSWORD", "")
    sender_name   = os.environ.get("SENDER_NAME", "Email Automation")

    if not sender_email or not sender_pass:
        msg = ("SMTP credentials missing. Open your .env file and set "
               "SENDER_EMAIL and SENDER_PASSWORD. "
               "Use a Gmail App Password, not your account password. "
               "See docs/phase_wise_guide.md Phase 5 for setup steps.")
        logger.error(f"SEND FAILED -> {to_email}: {msg}")
        result["status"]  = "failed"
        result["message"] = msg
        return result

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"]    = f"{sender_name} <{sender_email}>"
        msg["To"]      = to_email
        msg.attach(MIMEText(body, "plain", "utf-8"))

        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.ehlo()
            server.starttls()
            server.login(sender_email, sender_pass)
            server.sendmail(sender_email, to_email, msg.as_string())

        logger.info(f"SENT -> {to_email} | {subject}")
        result["status"]  = "sent"
        result["message"] = "Email sent successfully"

    except smtplib.SMTPAuthenticationError:
        err = "SMTP authentication failed. Check SENDER_EMAIL and SENDER_PASSWORD in .env"
        logger.error(f"AUTH ERROR -> {to_email}: {err}")
        result["status"]  = "failed"
        result["message"] = err

    except smtplib.SMTPException as e:
        logger.error(f"SMTP ERROR -> {to_email}: {e}")
        result["status"]  = "failed"
        result["message"] = str(e)

    except Exception as e:
        logger.error(f"ERROR -> {to_email}: {e}")
        result["status"]  = "failed"
        result["message"] = str(e)

    return result
