# ============================================================
# logger.py - Logging Setup
# Email Automation & Reminder System
# ============================================================

import logging
import os
from src.config import LOG_FILE, LOGS_DIR

def setup_logger():
    """Set up and return the project logger."""
    os.makedirs(LOGS_DIR, exist_ok=True)

    logger = logging.getLogger("EmailAutomation")
    logger.setLevel(logging.DEBUG)

    # Prevent duplicate handlers
    if logger.hasHandlers():
        logger.handlers.clear()

    # File handler
    file_handler = logging.FileHandler(LOG_FILE, mode='a', encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Formatter
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
