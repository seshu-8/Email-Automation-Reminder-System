# ============================================================
# template_engine.py - Load & Personalize Email Templates
# Email Automation & Reminder System
# ============================================================

import os
from src.config import TEMPLATES_DIR, TEMPLATE_MAP
from src.logger import setup_logger

logger = setup_logger()


def load_template(reminder_type: str) -> str:
    """Load email template based on reminder type."""
    reminder_type = str(reminder_type).lower().strip()
    filename = TEMPLATE_MAP.get(reminder_type)

    if not filename:
        logger.warning(f"⚠️ No template found for type '{reminder_type}'. Using default.")
        filename = "meeting_reminder.txt"  # fallback

    filepath = os.path.join(TEMPLATES_DIR, filename)

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        logger.debug(f"📄 Template loaded: {filename}")
        return content
    except FileNotFoundError:
        logger.error(f"❌ Template file not found: {filepath}")
        return ""
    except Exception as e:
        logger.error(f"❌ Error loading template: {e}")
        return ""


def personalize_email(template: str, row: dict) -> tuple:
    """
    Replace placeholders in template with actual contact/reminder data.
    Returns (subject, body) tuple.
    """
    try:
        # Extract subject from first line if present
        lines = template.strip().split("\n")
        subject = row.get("subject", "Reminder")
        body = template

        # Replace all {placeholders}
        for key, value in row.items():
            placeholder = "{" + str(key) + "}"
            body = body.replace(placeholder, str(value) if value else "N/A")

        # Remove "Subject: ..." first line from body
        body_lines = body.split("\n")
        if body_lines[0].startswith("Subject:"):
            body_lines = body_lines[2:]  # skip subject + blank line
        body = "\n".join(body_lines)

        logger.debug(f"✉️ Email personalized for {row.get('name', 'Unknown')}")
        return subject, body

    except Exception as e:
        logger.error(f"❌ Personalization failed: {e}")
        return "Reminder", template
