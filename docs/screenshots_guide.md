# Screenshots Guide — What to Capture & Where to Save

Save all screenshots inside the `images/` folder.
Name them exactly as shown below — they are referenced in README.md.

---

## Screenshot 1 — Project Folder Structure
**File:** `images/01_folder_structure.png`
**What to capture:** VS Code Explorer sidebar showing full folder tree
**How:** Open VS Code → open project folder → screenshot the left sidebar
**Shows:** data/, templates/, src/, outputs/, logs/, docs/, main.py, dashboard.py etc.

---

## Screenshot 2 — Contacts CSV
**File:** `images/02_contacts_csv.png`
**What to capture:** contacts.csv open in Excel or VS Code
**Shows:** 10 rows with name, email, company, role, phone columns

---

## Screenshot 3 — Reminders CSV
**File:** `images/03_reminders_csv.png`
**What to capture:** reminders.csv open in Excel or VS Code
**Shows:** 10 rows with reminder_id, type, subject, date, priority, status

---

## Screenshot 4 — Email Template
**File:** `images/04_email_template.png`
**What to capture:** meeting_reminder.txt open in VS Code
**Shows:** Template with {name}, {company}, {scheduled_date} placeholders visible

---

## Screenshot 5 — Dry-Run Terminal Output
**File:** `images/05_terminal_dryrun.png`
**What to capture:** Terminal after running `python main.py --mode all`
**Shows:**
```
EMAIL AUTOMATION SYSTEM
Mode: DRY-RUN
Processing 10 reminders...
[SIM]  Arjun Sharma    arjun.sharma@example.com
[SIM]  Priya Nair      priya.nair@example.com
...
Total Simulated: 10 | Failed: 0
```

---

## Screenshot 6 — Dashboard Overview Page
**File:** `images/06_dashboard_overview.png`
**What to capture:** Browser showing the Overview page at http://localhost:8501
**Shows:** 4 metric cards (10 contacts, 10 reminders, emails processed, 0 failed) + reminder breakdown bars

**How to capture:**
1. Run `streamlit run dashboard.py`
2. Open http://localhost:8501 in browser
3. Screenshot the full page

---

## Screenshot 7 — Run Automation Page
**File:** `images/07_dashboard_run.png`
**What to capture:** Browser showing Run Automation page AFTER clicking the button
**Shows:** Pipeline output panel filled with all 10 simulated emails and summary

---

## Screenshot 8 — Reports Page
**File:** `images/08_dashboard_reports.png`
**What to capture:** Browser showing Reports page with charts visible
**Shows:** Status distribution bar chart + reminder type bar chart + data table

---

## Screenshot 9 — Email Report CSV
**File:** `images/09_email_report.png`
**What to capture:** outputs/email_report.csv open in Excel
**Shows:** All 10 rows with reminder_id, name, email, status=simulated, timestamp

---

## Screenshot 10 — Log File
**File:** `images/10_log_file.png`
**What to capture:** logs/email_log.log open in VS Code or Notepad
**Shows:** Timestamped log entries for the run

---

## Screenshot 11 — GitHub Repo Preview
**File:** `images/11_github_repo.png`
**What to capture:** Your GitHub repository main page
**Shows:** Folder structure, README rendered, topics/tags, description

---

## Quick Capture Checklist

| # | Screenshot | Captured? |
|---|-----------|-----------|
| 01 | Folder structure | [ ] |
| 02 | Contacts CSV | [ ] |
| 03 | Reminders CSV | [ ] |
| 04 | Email template | [ ] |
| 05 | Terminal dry-run output | [ ] |
| 06 | Dashboard Overview | [ ] |
| 07 | Dashboard Run page | [ ] |
| 08 | Dashboard Reports | [ ] |
| 09 | Email report CSV | [ ] |
| 10 | Log file | [ ] |
| 11 | GitHub repo | [ ] |

---

## Windows Screenshot Shortcut
- Full screen: `Win + PrintScreen` → saved to Pictures/Screenshots
- Selected area: `Win + Shift + S` → draws selection → saves to clipboard → paste in Paint → save as PNG
