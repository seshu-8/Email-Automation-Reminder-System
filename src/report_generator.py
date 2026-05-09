# ============================================================
# report_generator.py - Generate CSV Report of Email Results
# Email Automation & Reminder System
# ============================================================

import os
import sys
import csv
from datetime import datetime

# Windows UTF-8 fix
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from src.config import REPORT_FILE, OUTPUTS_DIR
from src.logger import setup_logger

logger = setup_logger()


def save_report(results: list) -> str:
    """Save email sending results to a CSV report."""
    os.makedirs(OUTPUTS_DIR, exist_ok=True)

    fieldnames = [
        "reminder_id", "name", "to_email", "subject",
        "reminder_type", "priority", "status", "message", "timestamp"
    ]

    try:
        with open(REPORT_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for row in results:
                writer.writerow({k: row.get(k, "") for k in fieldnames})

        logger.info(f"Report saved: {REPORT_FILE}")
        return REPORT_FILE

    except Exception as e:
        logger.error(f"Failed to save report: {e}")
        return ""


def print_summary(results: list):
    """Print a clean summary to terminal."""
    total     = len(results)
    sent      = sum(1 for r in results if r.get("status") == "sent")
    simulated = sum(1 for r in results if r.get("status") == "simulated")
    failed    = sum(1 for r in results if r.get("status") == "failed")

    print("")
    print("=" * 60)
    print("  EMAIL AUTOMATION - EXECUTION SUMMARY")
    print("=" * 60)
    print(f"  Total processed : {total}")
    print(f"  Sent            : {sent}")
    print(f"  Simulated       : {simulated}")
    print(f"  Failed          : {failed}")
    print("=" * 60)

    if failed > 0:
        print("")
        print("  FAILED EMAILS:")
        for r in results:
            if r.get("status") == "failed":
                print(f"    -> {r.get('to_email')} | {r.get('message')}")

    print("")
    print(f"  Report saved : outputs/email_report.csv")
    print(f"  Logs saved   : logs/email_log.log")
    print("")
