# 📅 Day-by-Day Proof Building Plan

## Day 1 — Setup & Structure
- Install Python, create venv, install requirements
- Create project folder structure
- Commit: `feat: initialize project structure and requirements`
- Screenshot: folder structure in VS Code or terminal

## Day 2 — Data & Templates
- Create contacts.csv with 10 dummy contacts
- Create reminders.csv with 10 reminders of different types
- Create all 6 email templates
- Commit: `feat: add sample contacts, reminders CSV and email templates`
- Screenshot: CSV files open in spreadsheet / VS Code

## Day 3 — Core Engine (data_loader + template_engine)
- Test data_loader.py (run merge_data, print output)
- Test template_engine.py (load + personalize one email)
- Commit: `feat: implement data loader and template personalization engine`
- Screenshot: terminal showing merged data + personalized email preview

## Day 4 — Email Sender + Scheduler
- Test email_sender.py in dry-run mode
- Test scheduler.py with all 3 modes (today/all/overdue)
- Run main.py --mode all
- Commit: `feat: implement SMTP sender and reminder scheduler`
- Screenshot: dry-run terminal output showing simulated emails

## Day 5 — Logging + Reports
- Check logs/email_log.log content
- Check outputs/email_report.csv content
- Run main.py and show full summary
- Commit: `feat: add logging system and CSV report generation`
- Screenshot: log file + report CSV

## Day 6 — Dashboard + GitHub Polish
- Run: streamlit run dashboard.py
- Screenshot each dashboard page
- Write README.md
- Add .env.example, .gitignore
- Push all to GitHub
- Commit: `feat: add streamlit dashboard, README, and GitHub documentation`
- Screenshot: GitHub repo main page
