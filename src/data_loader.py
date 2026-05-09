# ============================================================
# data_loader.py - Load Contacts & Reminders from CSV
# Email Automation & Reminder System
# ============================================================

import os
import pandas as pd
from src.config import CONTACTS_FILE, REMINDERS_FILE
from src.logger import setup_logger

logger = setup_logger()


def load_contacts():
    """Load contact list from contacts.csv"""
    try:
        df = pd.read_csv(CONTACTS_FILE)
        df.columns = df.columns.str.strip().str.lower()
        logger.info(f"Loaded {len(df)} contacts from {CONTACTS_FILE}")
        return df
    except FileNotFoundError:
        logger.error(f"contacts.csv not found at: {CONTACTS_FILE}")
        return pd.DataFrame()
    except Exception as e:
        logger.error(f"Failed to load contacts: {e}")
        return pd.DataFrame()


def load_reminders():
    """Load reminder list from reminders.csv"""
    try:
        df = pd.read_csv(REMINDERS_FILE)
        df.columns = df.columns.str.strip().str.lower()
        logger.info(f"Loaded {len(df)} reminders from {REMINDERS_FILE}")
        return df
    except FileNotFoundError:
        logger.error(f"reminders.csv not found at: {REMINDERS_FILE}")
        return pd.DataFrame()
    except Exception as e:
        logger.error(f"Failed to load reminders: {e}")
        return pd.DataFrame()


def merge_data():
    """Merge contacts and reminders on email field."""
    contacts  = load_contacts()
    reminders = load_reminders()

    if contacts.empty or reminders.empty:
        logger.warning("Cannot merge - one or both datasets are empty.")
        return pd.DataFrame()

    merged = pd.merge(
        reminders,
        contacts,
        left_on="contact_email",
        right_on="email",
        how="left"
    )
    logger.info(f"Merged dataset: {len(merged)} rows")
    return merged
