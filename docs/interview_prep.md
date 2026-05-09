# 🎯 Interview Preparation — Email Automation Project

---

## Q1. Explain your project.

I built an **Email Automation & Reminder System** in Python. The system reads a contact list and reminder schedule from CSV files, personalizes email content using type-specific templates (meeting, payment, deadline, etc.), and sends emails via SMTP. It includes dry-run simulation mode, logging, CSV report generation, and a Streamlit web dashboard for monitoring.

---

## Q2. Why did you build this project?

Email communication in companies is highly repetitive — HR sends interview reminders, finance sends payment alerts, operations sends meeting notifications. This project demonstrates Python can automate this entire workflow, applicable to Python Developer, Automation Engineer, HR Tech, and Operations roles.

---

## Q3. What is smtplib and how did you use it?

`smtplib` is Python's built-in library for SMTP email sending. I used it to connect to Gmail's SMTP server (smtp.gmail.com port 587), authenticate via environment variables, and send MIMEMultipart formatted emails with starttls() encryption.

---

## Q4. What is dry-run mode and why did you implement it?

Dry-run mode simulates the full email pipeline without sending real emails — printing recipient, subject, and body preview to terminal. Controlled via DRY_RUN environment variable. Useful for safe testing, template validation, and demo environments.

---

## Q5. How did you handle sensitive data like passwords?

Used python-dotenv to load credentials from a .env file excluded from GitHub via .gitignore. The repo only contains .env.example showing the structure. In production, credentials would use AWS Secrets Manager or environment injection via CI/CD pipelines.

---

## Q6. How does template personalization work?

Each template is a .txt file with placeholders like {name}, {company}, {scheduled_date}. The template_engine.py loads the correct template by reminder type, then replaces all placeholders with actual row data using Python's string .replace() method.

---

## Q7. How does the scheduling logic work?

scheduler.py filters the reminder DataFrame by three modes — today (date == today), overdue (date < today), all (all pending). Uses pandas pd.to_datetime() for date comparison and filters status == "pending" to skip processed reminders.

---

## Q8. How does logging work?

Python's logging module with two handlers: FileHandler writes DEBUG+ to logs/email_log.log with timestamps; StreamHandler prints INFO+ to console. Every action — data load, email sent/failed, report saved — is logged at appropriate levels.

---

## Q9. What does the Streamlit dashboard show?

Five sections: Overview (metrics, recent activity, type breakdown), Run Automation (configure and trigger pipeline), Contacts (searchable table), Reminders (filtered queue), Reports (charts + download), Logs (level-filtered log viewer).

---

## Q10. How would this work in a real company?

Deployed on a server, main.py runs as a cron job (e.g., 8 AM daily). Contact/reminder data pulled from a database instead of CSV. SMTP credentials managed via secrets manager. Dashboard hosted internally for HR/Operations teams to monitor campaigns.

**HR Pitch:** "I built a Python tool that automates sending hundreds of personalized reminder emails — saving Operations and HR teams hours of manual work. It includes a web dashboard so non-technical teams can use it without touching code."
