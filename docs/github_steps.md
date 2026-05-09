# GitHub Upload Guide — Email Automation & Reminder System

## Recommended Repository Details

| Field | Value |
|-------|-------|
| Repo Name | `Email-Automation-Reminder-System` |
| Description | Python email automation system with SMTP, CSV scheduling, dry-run simulation, logging, and Streamlit dashboard |
| Visibility | Public |
| Topics/Tags | `python` `automation` `email` `smtp` `streamlit` `pandas` `csv` `reminder` `scheduler` `beginner-project` |

---

## Step-by-Step GitHub Upload

### Step 1 — Create Repository on GitHub

1. Go to https://github.com → click **New** (green button)
2. Repository name: `Email-Automation-Reminder-System`
3. Description: paste from table above
4. Set to **Public**
5. Do NOT check "Add README" (we already have one)
6. Click **Create repository**

---

### Step 2 — Initialize Git in Your Project Folder

Open terminal inside your project folder and run:

```bash
git init
```

---

### Step 3 — Add .gitignore First (IMPORTANT)

Verify .gitignore exists and contains `.env`:

```bash
cat .gitignore
```

You should see `.env` listed. If not, add it:

```bash
echo ".env" >> .gitignore
```

---

### Step 4 — Stage All Files

```bash
git add .
```

Verify what will be uploaded (check .env is NOT listed):

```bash
git status
```

If `.env` appears in the list, stop and fix .gitignore before continuing.

---

### Step 5 — First Commit

```bash
git commit -m "feat: initial commit — email automation & reminder system"
```

---

### Step 6 — Connect to GitHub

Copy the repo URL from GitHub (looks like https://github.com/YOUR_USERNAME/Email-Automation-Reminder-System.git)

```bash
git remote add origin https://github.com/YOUR_USERNAME/Email-Automation-Reminder-System.git
git branch -M main
git push -u origin main
```

---

### Step 7 — Add Topics/Tags on GitHub

1. Go to your repo page on GitHub
2. Click the gear icon next to **About**
3. Add these topics one by one:
   - python
   - automation
   - email
   - smtp
   - streamlit
   - pandas
   - csv
   - reminder
   - scheduler
   - beginner-project

---

## Commit Message Guide (Day-by-Day)

Use these exact commit messages to show clean professional history:

```bash
# Day 1
git commit -m "feat: initialize project structure and install requirements"

# Day 2
git commit -m "feat: add contacts CSV, reminders CSV, and 6 email templates"

# Day 3
git commit -m "feat: implement data_loader and template personalization engine"

# Day 4
git commit -m "feat: implement SMTP email sender with dry-run mode and scheduler"

# Day 5
git commit -m "feat: add logging system and CSV report generator"

# Day 6
git commit -m "feat: add streamlit dashboard with 6-page monitoring UI"

# Final polish
git commit -m "docs: add README, architecture diagram, interview prep, GitHub guide"
```

---

## What to Upload vs What NOT to Upload

### UPLOAD (safe)
- All `.py` files (main.py, dashboard.py, src/*.py)
- `data/contacts.csv` (dummy data only, no real emails)
- `data/reminders.csv`
- `templates/*.txt`
- `outputs/email_report.csv` (after a dry-run)
- `logs/email_log.log` (after a dry-run)
- `images/` (screenshots)
- `docs/` (all documentation)
- `README.md`
- `requirements.txt`
- `.env.example` (template only, no real passwords)
- `.gitignore`

### NEVER UPLOAD
- `.env` (real credentials — already in .gitignore)
- Any file containing your real Gmail password
- Any file containing real customer emails

---

## Push Updates After Changes

```bash
git add .
git commit -m "fix: resolve Windows Unicode encoding issue"
git push
```

---

## Verify Upload Checklist

After pushing, check your GitHub repo page:

- [ ] README.md renders with badges and formatting
- [ ] All folders visible: data/, templates/, src/, docs/, outputs/, logs/
- [ ] `.env` file is NOT visible (only `.env.example`)
- [ ] Topics/tags added
- [ ] Description filled in
- [ ] At least 6 commits with clean messages
- [ ] `outputs/email_report.csv` shows sample data
- [ ] `logs/email_log.log` shows timestamped entries
