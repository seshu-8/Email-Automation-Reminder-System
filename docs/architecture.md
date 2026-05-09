# System Architecture — Email Automation & Reminder System

## Text-Based Architecture Diagram

```
============================================================
         EMAIL AUTOMATION & REMINDER SYSTEM
              COMPLETE ARCHITECTURE
============================================================

INPUT LAYER
-----------
  contacts.csv          reminders.csv         templates/
  (name, email,         (reminder_id,         meeting_reminder.txt
   company, role,        contact_email,        payment_reminder.txt
   phone)                type, subject,        followup_reminder.txt
                         date, priority)       deadline_reminder.txt
                                               webinar_reminder.txt
                                               interview_reminder.txt
        |                     |                      |
        v                     v                      v
============================================================

PROCESSING LAYER — src/
-----------------------

  config.py
  (loads .env: SMTP creds, DRY_RUN flag, file paths)
        |
        v
  logger.py
  (sets up file + console logging → logs/email_log.log)
        |
        v
  data_loader.py
  ┌─────────────────────────────────┐
  │  load_contacts()                │
  │  load_reminders()               │
  │  merge_data()  ←── JOIN on email│
  └─────────────────────────────────┘
        |
        v
  scheduler.py
  ┌─────────────────────────────────┐
  │  get_due_reminders(mode)        │
  │    mode = today / all / overdue │
  │  filters: status == "pending"   │
  │  filters: scheduled_date match  │
  └─────────────────────────────────┘
        |
        v
  template_engine.py
  ┌─────────────────────────────────┐
  │  load_template(reminder_type)   │
  │    maps type → .txt file        │
  │  personalize_email(template,row)│
  │    replaces {name}, {company},  │
  │    {subject}, {date} etc.       │
  └─────────────────────────────────┘
        |
        v
  email_sender.py
  ┌─────────────────────────────────┐
  │  DRY_RUN = true?                │
  │    YES → simulate, print preview│
  │    NO  → smtplib SMTP connect   │
  │           starttls()            │
  │           login(email, password)│
  │           sendmail()            │
  │  returns: status dict           │
  └─────────────────────────────────┘
        |
        v
============================================================

OUTPUT LAYER
------------

  report_generator.py
  ┌─────────────────────────────────┐
  │  save_report(results)           │
  │    → outputs/email_report.csv   │
  │  print_summary()                │
  │    → terminal summary table     │
  └─────────────────────────────────┘

  outputs/email_report.csv          logs/email_log.log
  (reminder_id, name, email,        (timestamped entries
   subject, type, priority,          for every action,
   status, message, timestamp)       success, failure)

============================================================

CONTROL LAYER
-------------

  main.py (CLI)                     dashboard.py (Web UI)
  ┌──────────────────┐              ┌──────────────────────┐
  │ python main.py   │              │ streamlit run        │
  │  --mode today    │              │  dashboard.py        │
  │  --mode all      │              │                      │
  │  --mode overdue  │              │ Pages:               │
  │  --send          │              │  Overview (metrics)  │
  │                  │              │  Run Automation      │
  │ Calls all src/   │              │  Contacts            │
  │ modules in order │              │  Reminders           │
  └──────────────────┘              │  Reports (charts)    │
                                    │  Logs                │
                                    └──────────────────────┘

============================================================

DATA FLOW SUMMARY
-----------------

contacts.csv ─┐
              ├─→ merge_data() ─→ scheduler() ─→ template_engine()
reminders.csv ─┘                                        │
                                                        ↓
                                                 email_sender()
                                                /              \
                                          DRY RUN           REAL SMTP
                                         (simulate)         (Gmail)
                                               \              /
                                                ↓            ↓
                                           report_generator()
                                          /                  \
                                  email_report.csv      email_log.log

============================================================

SECURITY LAYER
--------------

  .env file (never uploaded to GitHub)
  ├── SENDER_EMAIL
  ├── SENDER_PASSWORD  (Gmail App Password)
  ├── SMTP_HOST
  ├── SMTP_PORT
  └── DRY_RUN

  .env.example (safe template uploaded to GitHub)
  .gitignore   (excludes .env, __pycache__, venv)

============================================================
```

## Module Responsibilities

| Module | Responsibility | Input | Output |
|--------|---------------|-------|--------|
| config.py | Load env vars, define paths | .env file | Config constants |
| logger.py | Setup logging | - | Logger object |
| data_loader.py | Read + merge CSVs | contacts.csv, reminders.csv | Merged DataFrame |
| scheduler.py | Filter by date/status | Merged DataFrame | Due reminders DataFrame |
| template_engine.py | Load + fill templates | Template file, row dict | subject, body strings |
| email_sender.py | Send or simulate email | to_email, subject, body | Result dict |
| report_generator.py | Save CSV + print summary | Results list | email_report.csv |
| main.py | CLI orchestrator | CLI args | Runs full pipeline |
| dashboard.py | Web UI | User interaction | Visual outputs |

## Common Beginner Mistakes Per Phase

| Phase | Mistake | Fix |
|-------|---------|-----|
| SMTP setup | Using Gmail password instead of App Password | Generate App Password in Google Account → Security |
| .env loading | Forgetting to call load_dotenv() | Always call it at top of config.py |
| CSV reading | Column name mismatch after merge | Use .str.strip().str.lower() on column names |
| Template | Placeholder typo {Name} vs {name} | Lowercase all keys in row_dict |
| Dry-run | DRY_RUN env not set | Set DRY_RUN=true in .env before running |
| Logging | Logger duplicating output | Check hasHandlers() before adding handlers |
| GitHub | Uploading real .env | Always verify .gitignore before git push |
