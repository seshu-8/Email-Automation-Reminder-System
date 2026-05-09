# ============================================================
# scheduler.py - Reminder Scheduling & Filtering
# Email Automation & Reminder System
# ============================================================

from datetime import datetime
import pandas as pd
from src.logger import setup_logger

logger = setup_logger()


def get_due_reminders(merged_df: pd.DataFrame, mode: str = "all") -> pd.DataFrame:
    """
    Filter reminders based on scheduling mode.
    Modes: 'today', 'all', 'overdue'
    """
    if merged_df.empty:
        logger.warning("No data to filter.")
        return pd.DataFrame()

    today = datetime.now().date()
    df = merged_df.copy()

    df["scheduled_date_parsed"] = pd.to_datetime(
        df["scheduled_date"], errors="coerce"
    ).dt.date

    # Only pending
    df = df[df["status"].str.strip().str.lower() == "pending"]

    if mode == "today":
        result = df[df["scheduled_date_parsed"] == today]
        logger.info(f"Today's reminders: {len(result)}")
    elif mode == "overdue":
        result = df[df["scheduled_date_parsed"] < today]
        logger.info(f"Overdue reminders: {len(result)}")
    else:  # all
        result = df
        logger.info(f"All pending reminders: {len(result)}")

    return result


def get_schedule_summary(merged_df: pd.DataFrame) -> dict:
    """Return summary counts by type, priority, status."""
    if merged_df.empty:
        return {}
    return {
        "total":       len(merged_df),
        "by_type":     merged_df["reminder_type"].value_counts().to_dict(),
        "by_priority": merged_df["priority"].value_counts().to_dict(),
        "by_status":   merged_df["status"].value_counts().to_dict(),
    }
