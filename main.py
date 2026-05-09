# ============================================================
# main.py - Entry Point
# Email Automation & Reminder System
# ============================================================

import sys
import os
import argparse
from datetime import datetime

# Windows UTF-8 fix - MUST be before any print
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Make src importable regardless of where script is run from
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

# Change working directory so CSV/template paths resolve correctly
os.chdir(BASE_DIR)

from src.logger import setup_logger
from src.data_loader import merge_data
from src.template_engine import load_template, personalize_email
from src.scheduler import get_due_reminders, get_schedule_summary
from src.report_generator import save_report, print_summary

logger = setup_logger()


def parse_args():
    parser = argparse.ArgumentParser(description="Email Automation & Reminder System")
    parser.add_argument(
        "--mode", choices=["today", "all", "overdue"], default="all",
        help="Which reminders to process"
    )
    parser.add_argument(
        "--send", action="store_true",
        help="Actually send emails via SMTP (default is dry-run)"
    )
    return parser.parse_args()


def main():
    args = parse_args()

    # Set DRY_RUN in environment BEFORE importing email_sender
    dry_run = not args.send
    os.environ["DRY_RUN"] = "true" if dry_run else "false"

    # Import email_sender AFTER env is set so it reads the correct value
    from src.email_sender import send_email

    mode_label = "DRY-RUN (simulation)" if dry_run else "LIVE SEND"

    print("")
    print("=" * 60)
    print("  EMAIL AUTOMATION & REMINDER SYSTEM")
    print(f"  Mode    : {mode_label}")
    print(f"  Filter  : {args.mode.upper()}")
    print(f"  Started : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print("")

    logger.info("=" * 50)
    logger.info("EMAIL AUTOMATION SYSTEM STARTED")
    logger.info(f"Mode: {'DRY-RUN' if dry_run else 'LIVE'} | Filter: {args.mode}")

    # Step 1: Load and merge data
    merged = merge_data()
    if merged.empty:
        logger.error("No data found. Exiting.")
        print("ERROR: No data loaded. Check data/contacts.csv and data/reminders.csv")
        return

    # Step 2: Summary
    summary = get_schedule_summary(merged)
    print(f"Reminders loaded : {summary.get('total', 0)}")
    print(f"By type          : {summary.get('by_type', {})}")
    print(f"By priority      : {summary.get('by_priority', {})}")
    print("")

    # Step 3: Filter
    due = get_due_reminders(merged, mode=args.mode)
    if due.empty:
        print(f"No '{args.mode}' reminders to process.")
        logger.info("No reminders matched the filter.")
        return

    print(f"Processing {len(due)} reminder(s)...")
    print("")

    # Step 4: Process each reminder
    results = []
    for _, row in due.iterrows():
        row_dict = row.to_dict()

        template = load_template(row_dict.get("reminder_type", "meeting"))
        if not template:
            logger.warning(f"Skipping {row_dict.get('contact_email')} - no template")
            continue

        subject, body = personalize_email(template, row_dict)

        result = send_email(
            to_email=str(row_dict.get("contact_email", "")),
            subject=str(subject),
            body=str(body),
            dry_run=dry_run
        )

        result["reminder_id"]   = row_dict.get("reminder_id", "")
        result["name"]          = row_dict.get("name", "Unknown")
        result["reminder_type"] = row_dict.get("reminder_type", "")
        result["priority"]      = row_dict.get("priority", "")
        result["timestamp"]     = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        results.append(result)

    # Step 5: Save report
    save_report(results)

    # Step 6: Print summary
    print_summary(results)

    logger.info("EMAIL AUTOMATION SYSTEM COMPLETED")
    logger.info("=" * 50)


if __name__ == "__main__":
    main()
