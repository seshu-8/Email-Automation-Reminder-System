# Phase-Wise Implementation Guide

## Phase 1 — Setup

**What to do:**
- Install Python 3.10+
- Install VS Code or any editor
- Create virtual environment
- Install required libraries

**Commands:**
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
pip install -r requirements.txt
```

**Why:** Virtual environment isolates your project dependencies so they don't conflict with other Python projects on your system.

**Expected output:** Terminal shows "Successfully installed pandas, streamlit, python-dotenv..."

**Common mistakes:**
- Not activating venv before pip install → libraries install globally, causing version conflicts
- Using Python 3.8 or below → some f-string and type hint syntax won't work

---

## Phase 2 — Project Folder Creation

**What to do:**
- Create the full folder structure as specified
- Create empty placeholder files in outputs/ and logs/

**Expected output:** Folder tree with data/, templates/, src/, outputs/, logs/, images/, docs/ all present

**Common mistakes:**
- Putting Python files directly in root instead of src/
- Missing __init__.py in src/ → imports between modules fail

---

## Phase 3 — Contact CSV Creation

**What to do:**
- Create `data/contacts.csv` with 10 dummy contacts
- Columns: name, email, company, role, phone

**Why:** Simulates a real company's employee or client database without needing actual CRM access.

**Expected output:** CSV opens in Excel/Sheets showing 10 rows, 5 columns

**Common mistakes:**
- Using real email addresses → risk of accidentally sending real emails in live mode
- Extra spaces in column headers → merge fails silently

---

## Phase 4 — Email Template Creation

**What to do:**
- Create 6 template files in templates/ folder
- Each uses {placeholder} syntax for personalization

**Why:** Template-based emails allow one codebase to handle all reminder types without hardcoded messages.

**Expected output:** 6 .txt files in templates/, each with {name}, {company}, {scheduled_date} placeholders

**Common mistakes:**
- Using different placeholder formats like [name] or %name% → personalization breaks
- Not adding a blank line after Subject: line → email body starts incorrectly

---

## Phase 5 — SMTP Configuration

**What to do:**
- Create `.env` file from `.env.example`
- Set SMTP_HOST, SMTP_PORT, SENDER_EMAIL, SENDER_PASSWORD
- Keep DRY_RUN=true until fully tested

**Gmail App Password setup:**
1. Go to myaccount.google.com
2. Security → 2-Step Verification → App Passwords
3. Generate password for "Mail"
4. Paste into SENDER_PASSWORD in .env

**Why:** SMTP (Simple Mail Transfer Protocol) is the standard email sending protocol. Gmail requires App Passwords (not your regular password) when using third-party apps.

**Expected output:** .env file exists locally, not visible on GitHub

**Common mistakes:**
- Using Gmail account password instead of App Password → authentication fails
- Committing .env to GitHub → security breach

---

## Phase 6 — Email Personalization

**What to do:**
- Run template_engine.py logic manually to test
- Verify {name} becomes "Arjun Sharma", {company} becomes "TechCorp India" etc.

**Test command:**
```python
from src.template_engine import load_template, personalize_email
template = load_template("meeting")
subject, body = personalize_email(template, {"name": "Test User", "company": "TestCo", "scheduled_date": "2025-05-10", "scheduled_time": "10:00", "subject": "Test Meeting"})
print(body)
```

**Expected output:** Fully filled email body with real values instead of placeholders

**Common mistakes:**
- Forgetting to pass all placeholder keys → unreplaced {placeholders} appear in email body
- Case mismatch {Name} vs {name} → placeholder not replaced

---

## Phase 7 — Reminder Scheduling

**What to do:**
- Test scheduler.py with all 3 modes
- Verify today/all/overdue filtering works correctly

**Test:**
```bash
python main.py --mode today
python main.py --mode all
python main.py --mode overdue
```

**Why:** Real companies send reminders on specific days — not all at once. Filtering by date ensures only relevant reminders are sent.

**Expected output:**
- `--mode today` → processes only today-dated reminders
- `--mode all` → processes all 10 pending reminders
- `--mode overdue` → processes past-dated reminders

**Common mistakes:**
- Date format mismatch in CSV (DD/MM/YYYY vs YYYY-MM-DD) → all reminders filtered out
- Status column not set to "pending" → no reminders pass filter

---

## Phase 8 — Email Sending (Dry-Run)

**What to do:**
- Run full pipeline in dry-run mode
- Verify each email is simulated in terminal output
- Check output shows To, Subject, Body for each contact

```bash
python main.py --mode all
```

**Expected output:**
```
[DRY-RUN] To: arjun.sharma@example.com | Subject: Team Sync Meeting Tomorrow
[DRY-RUN] To: priya.nair@example.com | Subject: Interview Reminder...
...
Total Processed: 10 | Simulated: 10 | Failed: 0
```

**Common mistakes:**
- DRY_RUN not set to true → tries real SMTP, fails if credentials not set
- Wrong working directory when running → CSV files not found

---

## Phase 9 — Logging and Report Generation

**What to do:**
- After running main.py, check logs/email_log.log
- Check outputs/email_report.csv
- Verify both files have correct data

**Expected log content:**
```
[2025-05-06 09:00:01] [INFO] Loaded 10 contacts
[2025-05-06 09:00:01] [INFO] Loaded 10 reminders
[2025-05-06 09:00:01] [INFO] [DRY-RUN] SIMULATED → arjun.sharma@example.com
...
```

**Expected report CSV columns:**
reminder_id, name, to_email, subject, reminder_type, priority, status, message, timestamp

**Common mistakes:**
- outputs/ or logs/ folder doesn't exist → FileNotFoundError (fixed by makedirs in code)
- Opening report CSV in Excel while Python writes to it → permission error on Windows

---

## Phase 10 — GitHub Upload

**What to do:**
- Follow docs/github_steps.md exactly
- Verify .env is NOT in the upload
- Add topics, description, and clean commit history

**Expected output:** Public GitHub repo with:
- Clean folder structure
- Working README with badges
- At least 6 commits with descriptive messages
- outputs/email_report.csv showing sample data
- logs/email_log.log with timestamped entries

**Common mistakes:**
- Not checking git status before commit → .env accidentally uploaded
- Single commit with all code → no visible development history (looks like copy-paste, not real work)
- No README → recruiter can't understand the project
