# 📧 Email Automation & Reminder System

> **Python project for automating email reminders using SMTP, CSV data, scheduling, and a Streamlit dashboard.**

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red?logo=streamlit)
![Status](https://img.shields.io/badge/Status-Complete-green)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

---

## 🧩 Problem Statement

Companies, HR teams, sales teams, and trainers manually send hundreds of reminder emails — meeting alerts, payment reminders, interview notifications, deadline alerts. This is time-consuming and error-prone.

This system **automates the entire pipeline** — from reading a contact list, personalizing messages, scheduling reminders, sending emails via SMTP, and generating reports.

---

## 🏭 Industry Relevance

| Use Case | Who Benefits |
|----------|-------------|
| Meeting reminders | Operations, Admin |
| Interview scheduling | HR Teams |
| Payment follow-ups | Finance, Sales |
| Deadline alerts | Project Management |
| Webinar invites | Training Teams |
| Client follow-ups | Business Development |

---

## ✨ Features

- 📋 Read contacts from CSV
- ⏰ Schedule reminders by date/type/priority
- ✉️ Personalized email generation from templates
- 📧 SMTP email sending (Gmail)
- 🔵 **Dry-Run mode** — simulate without sending real emails
- 📊 CSV report generation (sent/failed/simulated)
- 📜 Full logging with timestamp
- 🖥️ **Streamlit dashboard** — run, monitor, analyze in browser
- 🔒 Secure credential handling via `.env`

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.10+ | Core language |
| pandas | CSV data processing |
| smtplib | Email sending |
| email.mime | Email formatting |
| python-dotenv | Secure env variables |
| schedule | Reminder scheduling |
| streamlit | Web dashboard |
| logging | System logs |

---

## 📁 Folder Structure

```
Email-Automation-Reminder-System/
├── data/
│   ├── contacts.csv       ← Contact list
│   └── reminders.csv      ← Scheduled reminders
├── templates/
│   ├── meeting_reminder.txt
│   ├── payment_reminder.txt
│   ├── followup_reminder.txt
│   ├── deadline_reminder.txt
│   ├── webinar_reminder.txt
│   └── interview_reminder.txt
├── src/
│   ├── config.py          ← Config & env loader
│   ├── logger.py          ← Logging setup
│   ├── data_loader.py     ← CSV reader & merger
│   ├── template_engine.py ← Template loader & personalizer
│   ├── email_sender.py    ← SMTP sender (real + dry-run)
│   ├── scheduler.py       ← Reminder filter/scheduler
│   └── report_generator.py← CSV report + terminal summary
├── outputs/
│   └── email_report.csv   ← Generated after run
├── logs/
│   └── email_log.log      ← System logs
├── dashboard.py           ← Streamlit dashboard
├── main.py                ← CLI entry point
├── requirements.txt
├── .env.example           ← Template — copy to .env
├── .gitignore
└── README.md
```

---

## 🚀 Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/Email-Automation-Reminder-System.git
cd Email-Automation-Reminder-System
```

### 2. Create virtual environment
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
```bash
cp .env.example .env
# Edit .env with your Gmail credentials
```

> ⚠️ For Gmail: Use an **App Password**, not your regular password.
> Go to: Google Account → Security → 2-Step Verification → App Passwords

---

## ▶️ How to Run

### CLI Mode
```bash
# Dry-run (simulation) — all reminders
python main.py

# Dry-run — today's reminders only
python main.py --mode today

# Real email send — all reminders
python main.py --send

# Real email send — overdue only
python main.py --mode overdue --send
```

### Dashboard Mode
```bash
streamlit run dashboard.py
```
Then open: `http://localhost:8501`

---

## 📊 Sample Output

```
============================================================
   📧 EMAIL AUTOMATION & REMINDER SYSTEM
   Mode    : DRY-RUN (simulation)
   Filter  : ALL
============================================================

📋 Total Reminders Loaded: 10
   By Type    : {'meeting': 2, 'payment': 2, ...}

⏰ Processing 10 reminder(s)...

============================================================
  [DRY-RUN] EMAIL SIMULATION
============================================================
  To      : arjun.sharma@example.com
  Subject : Team Sync Meeting Tomorrow
  Body    : Dear Arjun Sharma, This is a reminder...
============================================================

============================================================
   📊 EMAIL AUTOMATION — EXECUTION SUMMARY
============================================================
   Total Processed : 10
   ✅ Sent          : 0
   🔵 Simulated     : 10
   ❌ Failed        : 0
============================================================
```

---

## 🔐 Security Notes

- Never upload `.env` to GitHub (already in `.gitignore`)
- Use `.env.example` for sharing config structure
- Use Gmail App Passwords, not account passwords

---

## 📚 Learning Outcomes

- File I/O with pandas and CSV
- OOP / modular Python programming
- SMTP email automation
- Template-based personalization
- Scheduling and filtering logic
- Logging and error handling
- Environment variable security
- Streamlit dashboard development
- GitHub documentation

---

## 👤 Author

**Seshu**  
Student | Python & Automation Learner  
📍 Andhra Pradesh, India

---

## 📄 License

MIT License — free to use and modify

---

## 📚 Documentation Index

| File | Description |
|------|-------------|
| [Architecture Diagram](docs/architecture.md) | Full system architecture diagram and end-to-end data flow explanation |
| [Phase-Wise Build Guide](docs/phase_wise_guide.md) | 10-phase build guide with expected outputs, checkpoints, and common mistakes |
| [GitHub Upload Guide](docs/github_steps.md) | Step-by-step GitHub upload guide with recommended commit messages |
| [Proof Building Plan](docs/proof_plan.md) | 6-day proof-building plan with daily development and commit targets |
| [Interview Preparation](docs/interview_prep.md) | 10 interview Q&As covering HR, project explanation, and technical discussions |
| [Screenshots Guide](docs/screenshots_guide.md) | Detailed guide on what screenshots to capture and where to save them |
