# ============================================================
# config.py - Configuration & Environment Variable Loader
# Email Automation & Reminder System
# ============================================================

import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# ---- SMTP CONFIG ----
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "your_email@gmail.com")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD", "your_app_password")
SENDER_NAME = os.getenv("SENDER_NAME", "Automation System")

# ---- FILE PATHS ----
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")
LOGS_DIR = os.path.join(BASE_DIR, "logs")

CONTACTS_FILE = os.path.join(DATA_DIR, "contacts.csv")
REMINDERS_FILE = os.path.join(DATA_DIR, "reminders.csv")
REPORT_FILE = os.path.join(OUTPUTS_DIR, "email_report.csv")
LOG_FILE = os.path.join(LOGS_DIR, "email_log.log")

# ---- TEMPLATE MAP ----
TEMPLATE_MAP = {
    "meeting":  "meeting_reminder.txt",
    "payment":  "payment_reminder.txt",
    "followup": "followup_reminder.txt",
    "deadline": "deadline_reminder.txt",
    "webinar":  "webinar_reminder.txt",
    "interview":"interview_reminder.txt",
}

# ---- SETTINGS ----
DRY_RUN = os.getenv("DRY_RUN", "true").lower() == "true"
