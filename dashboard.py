# ============================================================
# dashboard.py - Streamlit Dashboard
# Email Automation & Reminder System
# ============================================================
# Run: streamlit run dashboard.py
# ============================================================

import streamlit as st
import pandas as pd
import os
import sys
import json
import time
from datetime import datetime

# Make src importable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ---- PAGE CONFIG ----
st.set_page_config(
    page_title="Email Automation System",
    page_icon="📧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---- CUSTOM CSS ----
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --bg: #0a0e1a;
    --surface: #111827;
    --surface2: #1a2235;
    --border: #1e2d45;
    --accent: #3b82f6;
    --accent2: #8b5cf6;
    --green: #10b981;
    --red: #ef4444;
    --yellow: #f59e0b;
    --text: #e2e8f0;
    --muted: #64748b;
}

html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

.stApp { background: var(--bg) !important; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}

/* Cards */
.metric-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px 24px;
    position: relative;
    overflow: hidden;
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--accent), var(--accent2));
}
.metric-num {
    font-size: 2.4rem;
    font-weight: 700;
    line-height: 1;
    margin-bottom: 4px;
}
.metric-label {
    font-size: 0.8rem;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

/* Status badges */
.badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 999px;
    font-size: 0.72rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
.badge-sent      { background: rgba(16,185,129,0.15); color: #10b981; border: 1px solid rgba(16,185,129,0.3); }
.badge-simulated { background: rgba(59,130,246,0.15); color: #3b82f6; border: 1px solid rgba(59,130,246,0.3); }
.badge-failed    { background: rgba(239,68,68,0.15); color: #ef4444; border: 1px solid rgba(239,68,68,0.3); }
.badge-pending   { background: rgba(245,158,11,0.15); color: #f59e0b; border: 1px solid rgba(245,158,11,0.3); }
.badge-high      { background: rgba(239,68,68,0.12); color: #ef4444; }
.badge-medium    { background: rgba(245,158,11,0.12); color: #f59e0b; }
.badge-low       { background: rgba(100,116,139,0.12); color: #94a3b8; }

/* Section headers */
.section-title {
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    color: var(--muted);
    margin-bottom: 12px;
    padding-bottom: 8px;
    border-bottom: 1px solid var(--border);
}

/* Log output */
.log-box {
    background: #060a14;
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 16px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    color: #94a3b8;
    max-height: 320px;
    overflow-y: auto;
    line-height: 1.6;
}
.log-success { color: #10b981; }
.log-error   { color: #ef4444; }
.log-info    { color: #3b82f6; }
.log-warn    { color: #f59e0b; }

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #3b82f6, #8b5cf6) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    padding: 10px 20px !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 24px rgba(59,130,246,0.3) !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: var(--surface) !important;
    border-radius: 10px !important;
    border: 1px solid var(--border) !important;
    gap: 2px !important;
    padding: 4px !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--muted) !important;
    border-radius: 7px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 500 !important;
}
.stTabs [aria-selected="true"] {
    background: var(--surface2) !important;
    color: var(--text) !important;
}

/* DataFrames */
[data-testid="stDataFrame"] { border-radius: 10px !important; overflow: hidden; }

/* Inputs/selects */
.stSelectbox > div > div, .stRadio > div {
    background: var(--surface) !important;
    border-color: var(--border) !important;
    color: var(--text) !important;
}

/* Hide Streamlit branding */
#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# HELPER FUNCTIONS
# ============================================================

@st.cache_data(ttl=5)
def load_contacts():
    path = os.path.join(os.path.dirname(__file__), "data", "contacts.csv")
    try:
        return pd.read_csv(path)
    except:
        return pd.DataFrame()

@st.cache_data(ttl=5)
def load_reminders():
    path = os.path.join(os.path.dirname(__file__), "data", "reminders.csv")
    try:
        return pd.read_csv(path)
    except:
        return pd.DataFrame()

@st.cache_data(ttl=5)
def load_report():
    path = os.path.join(os.path.dirname(__file__), "outputs", "email_report.csv")
    try:
        return pd.read_csv(path)
    except:
        return pd.DataFrame()

def load_logs():
    path = os.path.join(os.path.dirname(__file__), "logs", "email_log.log")
    try:
        with open(path, "r") as f:
            return f.readlines()[-60:]  # last 60 lines
    except:
        return []

def colorize_log(line):
    line = line.strip()
    if "[ERROR]" in line:
        return f'<span class="log-error">{line}</span>'
    elif "[WARNING]" in line:
        return f'<span class="log-warn">{line}</span>'
    elif "✅" in line or "sent" in line.lower():
        return f'<span class="log-success">{line}</span>'
    elif "[INFO]" in line:
        return f'<span class="log-info">{line}</span>'
    else:
        return line

def run_automation(mode, dry_run):
    """Run automation pipeline directly (no subprocess) — works on all OS."""
    import io
    import importlib
    from contextlib import redirect_stdout

    base_dir = os.path.dirname(os.path.abspath(__file__))
    if base_dir not in sys.path:
        sys.path.insert(0, base_dir)

    # Set env before importing config
    os.environ["DRY_RUN"] = "true" if dry_run else "false"

    output_lines = []

    try:
        # Force reload config so DRY_RUN is picked up fresh
        import src.config as cfg
        importlib.reload(cfg)
        import src.email_sender as sender
        importlib.reload(sender)

        from src.data_loader import merge_data
        from src.template_engine import load_template, personalize_email
        from src.email_sender import send_email
        from src.scheduler import get_due_reminders, get_schedule_summary
        from src.report_generator import save_report

        mode_label = "DRY-RUN (simulation)" if dry_run else "LIVE SEND"
        output_lines.append(f"{'='*56}")
        output_lines.append(f"  EMAIL AUTOMATION SYSTEM")
        output_lines.append(f"  Mode   : {mode_label}")
        output_lines.append(f"  Filter : {mode.upper()}")
        output_lines.append(f"  Time   : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        output_lines.append(f"{'='*56}")
        output_lines.append("")

        merged = merge_data()
        if merged.empty:
            output_lines.append("ERROR: No data loaded. Check data/contacts.csv and data/reminders.csv")
            return "\n".join(output_lines)

        summary = get_schedule_summary(merged)
        output_lines.append(f"Contacts loaded : {len(merged['contact_email'].unique())}")
        output_lines.append(f"Reminders loaded: {summary.get('total', 0)}")
        output_lines.append(f"By type  : {summary.get('by_type', {})}")
        output_lines.append(f"By priority: {summary.get('by_priority', {})}")
        output_lines.append("")

        due = get_due_reminders(merged, mode=mode)
        if due.empty:
            output_lines.append(f"No '{mode}' reminders to process right now.")
            return "\n".join(output_lines)

        output_lines.append(f"Processing {len(due)} reminder(s)...")
        output_lines.append("")

        results = []
        for _, row in due.iterrows():
            row_dict = row.to_dict()
            template = load_template(row_dict.get("reminder_type", "meeting"))
            if not template:
                output_lines.append(f"  SKIP: no template for {row_dict.get('contact_email')}")
                continue

            subject, body = personalize_email(template, row_dict)
            result = send_email(
                to_email=row_dict.get("contact_email", ""),
                subject=subject,
                body=body
            )
            result["reminder_id"]   = row_dict.get("reminder_id", "")
            result["name"]          = row_dict.get("name", "Unknown")
            result["reminder_type"] = row_dict.get("reminder_type", "")
            result["priority"]      = row_dict.get("priority", "")
            result["timestamp"]     = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            results.append(result)

            status_icon = {"sent":"[SENT]","simulated":"[SIM] ","failed":"[FAIL]"}.get(result["status"],"[----]")
            output_lines.append(f"  {status_icon}  {result.get('name','?'):<18}  {row_dict.get('contact_email','')}")
            output_lines.append(f"           Subject : {subject}")
            output_lines.append(f"           Type    : {row_dict.get('reminder_type','')}  |  Priority: {row_dict.get('priority','')}")
            if result["status"] == "failed":
                output_lines.append(f"           ERROR   : {result.get('message','')}")
            output_lines.append("")

        save_report(results)

        sent      = sum(1 for r in results if r["status"] == "sent")
        simulated = sum(1 for r in results if r["status"] == "simulated")
        failed    = sum(1 for r in results if r["status"] == "failed")

        output_lines.append(f"{'='*56}")
        output_lines.append(f"  SUMMARY")
        output_lines.append(f"{'='*56}")
        output_lines.append(f"  Total Processed : {len(results)}")
        output_lines.append(f"  Sent            : {sent}")
        output_lines.append(f"  Simulated       : {simulated}")
        output_lines.append(f"  Failed          : {failed}")
        output_lines.append(f"{'='*56}")
        output_lines.append(f"  Report saved to : outputs/email_report.csv")
        output_lines.append(f"  Logs saved to   : logs/email_log.log")

        return "\n".join(output_lines)

    except Exception as e:
        import traceback
        output_lines.append(f"PIPELINE ERROR: {e}")
        output_lines.append(traceback.format_exc())
        return "\n".join(output_lines)

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown("""
    <div style='padding: 8px 0 20px'>
        <div style='font-size:1.4rem; font-weight:700; letter-spacing:-0.02em'>📧 EmailBot</div>
        <div style='font-size:0.75rem; color:#64748b; margin-top:4px'>Automation & Reminder System</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">Navigation</div>', unsafe_allow_html=True)
    page = st.radio(
        "", 
        ["🏠 Overview", "🚀 Run Automation", "📋 Contacts", "⏰ Reminders", "📊 Reports", "📜 Logs"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown('<div class="section-title">Quick Stats</div>', unsafe_allow_html=True)

    contacts_df = load_contacts()
    reminders_df = load_reminders()
    report_df = load_report()

    st.markdown(f"👥 **{len(contacts_df)}** Contacts")
    st.markdown(f"⏰ **{len(reminders_df)}** Reminders")
    st.markdown(f"📨 **{len(report_df)}** Emails Processed")

    st.markdown("---")
    now = datetime.now()
    st.markdown(f"""
    <div style='font-size:0.72rem; color:#475569; line-height:1.8'>
    🕐 {now.strftime('%H:%M:%S')}<br>
    📅 {now.strftime('%d %b %Y')}<br>
    🐍 Python Email System
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# PAGE: OVERVIEW
# ============================================================

if page == "🏠 Overview":
    st.markdown("""
    <div style='margin-bottom: 28px'>
        <h1 style='font-size:1.9rem; font-weight:700; margin:0; letter-spacing:-0.03em'>
            Email Automation Dashboard
        </h1>
        <p style='color:#64748b; margin:6px 0 0; font-size:0.9rem'>
            Monitor, run, and analyze your automated reminder system
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ---- METRIC CARDS ----
    c1, c2, c3, c4 = st.columns(4)

    sent = len(report_df[report_df["status"]=="sent"]) if not report_df.empty and "status" in report_df.columns else 0
    sim = len(report_df[report_df["status"]=="simulated"]) if not report_df.empty and "status" in report_df.columns else 0
    fail = len(report_df[report_df["status"]=="failed"]) if not report_df.empty and "status" in report_df.columns else 0

    with c1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-num" style="color:#3b82f6">{len(contacts_df)}</div>
            <div class="metric-label">Total Contacts</div>
        </div>""", unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-num" style="color:#8b5cf6">{len(reminders_df)}</div>
            <div class="metric-label">Reminders Queued</div>
        </div>""", unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-num" style="color:#10b981">{sent + sim}</div>
            <div class="metric-label">Emails Processed</div>
        </div>""", unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-num" style="color:#ef4444">{fail}</div>
            <div class="metric-label">Failed Sends</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ---- TWO COLUMNS ----
    left, right = st.columns([1.2, 1])

    with left:
        st.markdown('<div class="section-title">Recent Activity</div>', unsafe_allow_html=True)
        if not report_df.empty:
            display = report_df[["name","to_email","reminder_type","priority","status"]].tail(8)
            
            rows_html = ""
            for _, r in display.iterrows():
                s = str(r.get("status","")).lower()
                p = str(r.get("priority","")).lower()
                sbadge = f'<span class="badge badge-{s}">{s}</span>'
                pbadge = f'<span class="badge badge-{p}">{p}</span>'
                rows_html += f"""
                <tr style='border-bottom:1px solid #1e2d45'>
                    <td style='padding:10px 8px;font-weight:500'>{r.get('name','')}</td>
                    <td style='padding:10px 8px;color:#64748b;font-size:0.82rem'>{r.get('reminder_type','')}</td>
                    <td style='padding:10px 8px'>{pbadge}</td>
                    <td style='padding:10px 8px'>{sbadge}</td>
                </tr>"""

            st.markdown(f"""
            <table style='width:100%;border-collapse:collapse;font-size:0.85rem'>
                <thead>
                    <tr style='color:#475569;font-size:0.72rem;text-transform:uppercase;letter-spacing:.08em'>
                        <th style='padding:8px;text-align:left;font-weight:500'>Name</th>
                        <th style='padding:8px;text-align:left;font-weight:500'>Type</th>
                        <th style='padding:8px;text-align:left;font-weight:500'>Priority</th>
                        <th style='padding:8px;text-align:left;font-weight:500'>Status</th>
                    </tr>
                </thead>
                <tbody>{rows_html}</tbody>
            </table>
            """, unsafe_allow_html=True)
        else:
            st.info("No report data yet. Run the automation first.")

    with right:
        st.markdown('<div class="section-title">Reminder Breakdown</div>', unsafe_allow_html=True)
        if not reminders_df.empty:
            type_counts = reminders_df["reminder_type"].value_counts()
            for rtype, cnt in type_counts.items():
                pct = int(cnt / len(reminders_df) * 100)
                icons = {"meeting":"📅","payment":"💳","followup":"📩","deadline":"⚠️","webinar":"🎙️","interview":"👔"}
                icon = icons.get(rtype, "📧")
                st.markdown(f"""
                <div style='margin-bottom:12px'>
                    <div style='display:flex;justify-content:space-between;margin-bottom:5px'>
                        <span style='font-size:0.85rem'>{icon} {rtype.title()}</span>
                        <span style='font-size:0.8rem;color:#64748b'>{cnt}</span>
                    </div>
                    <div style='background:#1a2235;border-radius:4px;height:6px'>
                        <div style='background:linear-gradient(90deg,#3b82f6,#8b5cf6);height:6px;
                                    border-radius:4px;width:{pct}%'></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # ---- RECENT LOGS ----
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">Recent Logs</div>', unsafe_allow_html=True)
    logs = load_logs()
    if logs:
        html = "<br>".join([colorize_log(l) for l in logs[-15:]])
        st.markdown(f'<div class="log-box">{html}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="log-box" style="color:#475569">No logs yet. Run automation to generate logs.</div>', unsafe_allow_html=True)

# ============================================================
# PAGE: RUN AUTOMATION
# ============================================================

elif page == "🚀 Run Automation":
    st.markdown("""
    <h2 style='font-size:1.6rem;font-weight:700;margin-bottom:6px'>Run Automation</h2>
    <p style='color:#64748b;font-size:0.9rem;margin-bottom:28px'>
        Configure and trigger your email automation pipeline
    </p>
    """, unsafe_allow_html=True)

    # ---- CREDENTIAL CHECK ----
    def check_credentials():
        from dotenv import load_dotenv
        base = os.path.dirname(os.path.abspath(__file__))
        load_dotenv(os.path.join(base, ".env"))
        email = os.environ.get("SENDER_EMAIL", "").strip()
        pwd   = os.environ.get("SENDER_PASSWORD", "").strip()
        ok = bool(email and pwd
                  and email != "your_email@gmail.com"
                  and pwd   != "your_app_password"
                  and "@" in email)
        return ok, email

    creds_ok, creds_email = check_credentials()

    col1, col2 = st.columns([1, 1.2])

    with col1:
        st.markdown('<div class="section-title">Configuration</div>', unsafe_allow_html=True)

        run_mode = st.selectbox(
            "Reminder Filter",
            ["all", "today", "overdue"],
            format_func=lambda x: {"all":"All Pending", "today":"Today Only", "overdue":"Overdue Only"}[x]
        )

        dry_run = st.toggle("Dry-Run Mode (Simulate — no real emails sent)", value=True)

        st.markdown("<br>", unsafe_allow_html=True)

        if dry_run:
            st.markdown("""
            <div style='background:rgba(59,130,246,0.08);border:1px solid rgba(59,130,246,0.25);
                        border-radius:8px;padding:14px 16px;font-size:0.83rem'>
            <span style='color:#60a5fa;font-weight:600'>DRY-RUN MODE</span><br>
            <span style='color:#94a3b8;margin-top:4px;display:block'>
            Emails are simulated — nothing is sent. Safe for testing, demos, and GitHub screenshots.
            </span>
            </div>
            """, unsafe_allow_html=True)
        else:
            if creds_ok:
                st.markdown(f"""
                <div style='background:rgba(16,185,129,0.08);border:1px solid rgba(16,185,129,0.25);
                            border-radius:8px;padding:14px 16px;font-size:0.83rem'>
                <span style='color:#34d399;font-weight:600'>LIVE MODE — Credentials Found</span><br>
                <span style='color:#94a3b8;margin-top:4px;display:block'>
                Sending as: <code style='color:#6ee7b7'>{creds_email}</code><br>
                Real emails will be sent via Gmail SMTP.
                </span>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style='background:rgba(239,68,68,0.08);border:1px solid rgba(239,68,68,0.3);
                            border-radius:8px;padding:14px 16px;font-size:0.83rem'>
                <span style='color:#f87171;font-weight:600'>LIVE MODE — No Credentials</span><br>
                <span style='color:#94a3b8;margin-top:4px;display:block'>
                Your .env file is missing or has placeholder values.<br>
                Set up credentials below, then re-run.
                </span>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        btn_disabled = (not dry_run and not creds_ok)
        if btn_disabled:
            st.button("Run Automation Pipeline", disabled=True, use_container_width=True)
            st.caption("Set up SMTP credentials below to enable Live Mode.")
        else:
            if st.button("Run Automation Pipeline", use_container_width=True):
                with st.spinner("Processing reminders..."):
                    output = run_automation(run_mode, dry_run)
                    st.session_state["last_output"] = output
                    st.session_state["last_run"] = datetime.now().strftime("%H:%M:%S")
                    load_report.clear()
                    load_contacts.clear()
                    load_reminders.clear()
                has_fail = "PIPELINE ERROR" in output or ("[FAIL]" in output and "SMTP credentials" in output)
                if has_fail:
                    st.error("Errors found. See output panel.")
                else:
                    st.success(f"Done at {st.session_state.get('last_run')} — check Reports & Overview.")

        # ---- SMTP SETUP GUIDE ----
        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("Setup SMTP credentials (.env)"):
            st.markdown("""
            <div style='font-size:0.83rem;line-height:1.8;color:#94a3b8'>
            <b style='color:#e2e8f0'>Step 1 — Get Gmail App Password</b><br>
            1. Go to <a href='https://myaccount.google.com/security' target='_blank' style='color:#60a5fa'>myaccount.google.com/security</a><br>
            2. Enable 2-Step Verification<br>
            3. Search "App passwords" → select Mail → Generate<br>
            4. Copy the 16-character password shown<br><br>

            <b style='color:#e2e8f0'>Step 2 — Edit your .env file</b><br>
            Open <code>.env</code> in your project folder and fill in:
            </div>
            """, unsafe_allow_html=True)

            st.code("""SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=youremail@gmail.com
SENDER_PASSWORD=abcd efgh ijkl mnop
SENDER_NAME=Email Automation System
DRY_RUN=false""", language="bash")

            st.markdown("""
            <div style='font-size:0.8rem;color:#64748b;margin-top:8px'>
            After saving .env, refresh this page — credentials will be detected automatically.
            </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="section-title">Pipeline Output</div>', unsafe_allow_html=True)
        output = st.session_state.get("last_output", "")
        if output:
            lines = output.split("\n")
            colored = []
            for line in lines:
                if "❌" in line or "failed" in line.lower() or "error" in line.lower():
                    colored.append(f'<span class="log-error">{line}</span>')
                elif "✅" in line or "sent" in line.lower() or "simulated" in line.lower():
                    colored.append(f'<span class="log-success">{line}</span>')
                elif "⚠️" in line or "warning" in line.lower():
                    colored.append(f'<span class="log-warn">{line}</span>')
                elif "=" in line:
                    colored.append(f'<span style="color:#334155">{line}</span>')
                else:
                    colored.append(line)
            html = "<br>".join(colored)
            st.markdown(f'<div class="log-box" style="max-height:500px">{html}</div>', unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="log-box" style="color:#334155;text-align:center;padding:60px 20px">
                No output yet.<br>Configure and click Run to start.
            </div>
            """, unsafe_allow_html=True)

# ============================================================
# PAGE: CONTACTS
# ============================================================

elif page == "📋 Contacts":
    st.markdown("""
    <h2 style='font-size:1.6rem;font-weight:700;margin-bottom:6px'>Contact List</h2>
    <p style='color:#64748b;font-size:0.9rem;margin-bottom:28px'>
        Manage email recipients loaded from contacts.csv
    </p>
    """, unsafe_allow_html=True)

    df = load_contacts()

    if df.empty:
        st.warning("No contacts found. Check data/contacts.csv")
    else:
        # Filter
        search = st.text_input("🔍 Search by name, company or role...", placeholder="e.g. TechCorp")
        if search:
            mask = df.apply(lambda r: search.lower() in str(r).lower(), axis=1)
            df = df[mask]

        st.markdown(f"<div style='color:#64748b;font-size:0.82rem;margin-bottom:12px'>{len(df)} contacts</div>", unsafe_allow_html=True)
        st.dataframe(df, use_container_width=True, height=400)

        # Download
        csv = df.to_csv(index=False)
        st.download_button("⬇ Download Contacts CSV", csv, "contacts.csv", "text/csv")

# ============================================================
# PAGE: REMINDERS
# ============================================================

elif page == "⏰ Reminders":
    st.markdown("""
    <h2 style='font-size:1.6rem;font-weight:700;margin-bottom:6px'>Reminder Queue</h2>
    <p style='color:#64748b;font-size:0.9rem;margin-bottom:28px'>
        View and filter all scheduled reminders
    </p>
    """, unsafe_allow_html=True)

    df = load_reminders()

    if df.empty:
        st.warning("No reminders found. Check data/reminders.csv")
    else:
        c1, c2, c3 = st.columns(3)
        type_filter = c1.selectbox("Type", ["All"] + sorted(df["reminder_type"].unique().tolist()))
        priority_filter = c2.selectbox("Priority", ["All"] + sorted(df["priority"].unique().tolist()))
        status_filter = c3.selectbox("Status", ["All"] + sorted(df["status"].unique().tolist()))

        filtered = df.copy()
        if type_filter != "All": filtered = filtered[filtered["reminder_type"] == type_filter]
        if priority_filter != "All": filtered = filtered[filtered["priority"] == priority_filter]
        if status_filter != "All": filtered = filtered[filtered["status"] == status_filter]

        st.markdown(f"<div style='color:#64748b;font-size:0.82rem;margin-bottom:12px'>{len(filtered)} reminders</div>", unsafe_allow_html=True)

        # Styled table
        rows_html = ""
        for _, r in filtered.iterrows():
            p = str(r.get("priority","")).lower()
            s = str(r.get("status","")).lower()
            type_icons = {"meeting":"📅","payment":"💳","followup":"📩","deadline":"⚠️","webinar":"🎙️","interview":"👔"}
            icon = type_icons.get(str(r.get("reminder_type","")), "📧")
            rows_html += f"""
            <tr style='border-bottom:1px solid #1e2d45'>
                <td style='padding:10px 8px;font-family:JetBrains Mono,monospace;font-size:0.75rem;color:#475569'>{r.get('reminder_id','')}</td>
                <td style='padding:10px 8px'>{icon} {str(r.get('reminder_type','')).title()}</td>
                <td style='padding:10px 8px;font-size:0.83rem'>{r.get('contact_email','')}</td>
                <td style='padding:10px 8px;font-size:0.83rem'>{r.get('scheduled_date','')} {r.get('scheduled_time','')}</td>
                <td style='padding:10px 8px'><span class="badge badge-{p}">{p}</span></td>
                <td style='padding:10px 8px'><span class="badge badge-{s}">{s}</span></td>
            </tr>"""

        st.markdown(f"""
        <div style='overflow-x:auto'>
        <table style='width:100%;border-collapse:collapse;font-size:0.85rem'>
            <thead>
                <tr style='color:#475569;font-size:0.72rem;text-transform:uppercase;letter-spacing:.08em;border-bottom:1px solid #1e2d45'>
                    <th style='padding:10px 8px;text-align:left;font-weight:500'>ID</th>
                    <th style='padding:10px 8px;text-align:left;font-weight:500'>Type</th>
                    <th style='padding:10px 8px;text-align:left;font-weight:500'>Email</th>
                    <th style='padding:10px 8px;text-align:left;font-weight:500'>Scheduled</th>
                    <th style='padding:10px 8px;text-align:left;font-weight:500'>Priority</th>
                    <th style='padding:10px 8px;text-align:left;font-weight:500'>Status</th>
                </tr>
            </thead>
            <tbody>{rows_html}</tbody>
        </table>
        </div>
        """, unsafe_allow_html=True)

# ============================================================
# PAGE: REPORTS
# ============================================================

elif page == "📊 Reports":
    st.markdown("""
    <h2 style='font-size:1.6rem;font-weight:700;margin-bottom:6px'>Email Reports</h2>
    <p style='color:#64748b;font-size:0.9rem;margin-bottom:28px'>
        Analyze outcomes from past automation runs
    </p>
    """, unsafe_allow_html=True)

    df = load_report()

    if df.empty:
        st.info("No report yet. Run the automation pipeline first.")
    else:
        # Summary metrics
        c1, c2, c3, c4 = st.columns(4)
        status_counts = df["status"].value_counts() if "status" in df.columns else {}

        with c1:
            n = status_counts.get("sent", 0)
            st.markdown(f'<div class="metric-card"><div class="metric-num" style="color:#10b981">{n}</div><div class="metric-label">Sent</div></div>', unsafe_allow_html=True)
        with c2:
            n = status_counts.get("simulated", 0)
            st.markdown(f'<div class="metric-card"><div class="metric-num" style="color:#3b82f6">{n}</div><div class="metric-label">Simulated</div></div>', unsafe_allow_html=True)
        with c3:
            n = status_counts.get("failed", 0)
            st.markdown(f'<div class="metric-card"><div class="metric-num" style="color:#ef4444">{n}</div><div class="metric-label">Failed</div></div>', unsafe_allow_html=True)
        with c4:
            total = len(df)
            st.markdown(f'<div class="metric-card"><div class="metric-num" style="color:#8b5cf6">{total}</div><div class="metric-label">Total</div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Charts
        col_l, col_r = st.columns(2)

        with col_l:
            st.markdown('<div class="section-title">Status Distribution</div>', unsafe_allow_html=True)
            if "status" in df.columns:
                chart_df = df["status"].value_counts().reset_index()
                chart_df.columns = ["Status", "Count"]
                st.bar_chart(chart_df.set_index("Status"), color="#3b82f6")

        with col_r:
            st.markdown('<div class="section-title">By Reminder Type</div>', unsafe_allow_html=True)
            if "reminder_type" in df.columns:
                chart_df = df["reminder_type"].value_counts().reset_index()
                chart_df.columns = ["Type", "Count"]
                st.bar_chart(chart_df.set_index("Type"), color="#8b5cf6")

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-title">Full Report Table</div>', unsafe_allow_html=True)
        st.dataframe(df, use_container_width=True, height=350)

        csv = df.to_csv(index=False)
        st.download_button("⬇ Download Report CSV", csv, "email_report.csv", "text/csv")

# ============================================================
# PAGE: LOGS
# ============================================================

elif page == "📜 Logs":
    st.markdown("""
    <h2 style='font-size:1.6rem;font-weight:700;margin-bottom:6px'>System Logs</h2>
    <p style='color:#64748b;font-size:0.9rem;margin-bottom:28px'>
        Real-time log output from the automation engine
    </p>
    """, unsafe_allow_html=True)

    logs = load_logs()

    filter_col, btn_col = st.columns([3,1])
    level_filter = filter_col.selectbox("Filter Level", ["All", "INFO", "ERROR", "WARNING", "DEBUG"])

    if btn_col.button("🔄 Refresh", use_container_width=True):
        st.rerun()

    if logs:
        filtered_logs = logs
        if level_filter != "All":
            filtered_logs = [l for l in logs if f"[{level_filter}]" in l]

        colored = [colorize_log(l) for l in filtered_logs]
        html = "<br>".join(colored)
        st.markdown(f'<div class="log-box" style="max-height:600px">{html}</div>', unsafe_allow_html=True)
        st.markdown(f"<div style='color:#475569;font-size:0.75rem;margin-top:8px'>{len(filtered_logs)} log entries</div>", unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="log-box" style="color:#334155;text-align:center;padding:80px">
            No logs yet. Run the automation pipeline to generate logs.
        </div>
        """, unsafe_allow_html=True)
