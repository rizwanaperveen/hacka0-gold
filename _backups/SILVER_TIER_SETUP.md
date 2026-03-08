# Silver Tier Setup Guide

Complete guide to implementing Silver Tier functionality for your AI Employee.

## Silver Tier Requirements

✅ All Bronze requirements plus:
- Two or more Watcher scripts (Gmail + WhatsApp + LinkedIn)
- Automatically post on LinkedIn for business/sales
- Claude reasoning loop that creates Plan.md files
- One working MCP server for external actions
- Human-in-the-loop approval workflow
- Basic scheduling via cron or Task Scheduler
- All AI functionality as Agent Skills

## Quick Start

### 1. Verify Bronze Tier Complete

Ensure you have:
- [ ] Obsidian vault with Dashboard.md and Company_Handbook.md
- [ ] Basic folder structure: /Inbox, /Needs_Action, /Done
- [ ] Claude Code working with the vault
- [ ] `/process-tasks` skill functional

### 2. Install Watcher Dependencies

```bash
cd watchers
pip install -r requirements.txt
playwright install chromium
```

### 3. Configure Watchers

#### Gmail Watcher
1. Set up Google Cloud project and Gmail API
2. Download OAuth credentials
3. Save to `watchers/credentials/gmail_credentials.json`
4. Run first time: `python gmail_watcher.py`
5. Authenticate in browser

#### WhatsApp Watcher
1. Run first time: `python whatsapp_watcher.py`
2. Scan QR code when browser opens
3. Session saved for future runs

#### LinkedIn Watcher
1. Run first time: `python linkedin_watcher.py`
2. Log in when browser opens
3. Session saved for future runs

### 4. Start Watchers with PM2

```bash
npm install -g pm2

pm2 start watchers/gmail_watcher.py --interpreter python3 --name gmail
pm2 start watchers/whatsapp_watcher.py --interpreter python3 --name whatsapp
pm2 start watchers/linkedin_watcher.py --interpreter python3 --name linkedin

pm2 save
pm2 startup
```

### 5. Test Skills

```bash
cd AI_Employee_Vault

# Test task processing
claude /process-tasks

# Test plan creation
claude /create-plan "task: prepare monthly report"

# Test LinkedIn posting
claude /linkedin-post

# Test email sending
claude /send-email

# Test approval processing
claude /approve-actions
```

## Skills Overview

### Core Skills (Silver Tier)

| Skill | Purpose | Usage |
|-------|---------|-------|
| `/process-tasks` | Process items from Needs_Action | `claude /process-tasks` |
| `/create-plan` | Create detailed action plans | `claude /create-plan` |
| `/send-email` | Draft and send emails with approval | `claude /send-email` |
| `/linkedin-post` | Create and post LinkedIn content | `claude /linkedin-post` |
| `/approve-actions` | Execute approved actions | `claude /approve-actions` |

### Skill Locations

All skills are in: `AI_Employee_Vault/.claude/skills/`

```
.claude/skills/
├── process-tasks/
│   ├── SKILL.md
│   └── prompt.md
├── create-plan/
│   ├── SKILL.md
│   └── prompt.md
├── send-email/
│   ├── SKILL.md
│   └── prompt.md
├── linkedin-post/
│   ├── SKILL.md
│   └── prompt.md
├── approve-actions/
│   ├── SKILL.md
│   └── prompt.md
└── browsing-with-playwright/
    ├── SKILL.md
    └── scripts/
```

## Workflow Examples

### Example 1: Email Response Flow

1. **Watcher detects**: Gmail watcher finds important email
2. **Creates task**: `EMAIL_client_inquiry_abc123.md` in Needs_Action
3. **You run**: `claude /process-tasks`
4. **Claude analyzes**: Reads email context and Company_Handbook
5. **Creates plan**: Generates Plan.md with response strategy
6. **Drafts email**: Creates approval request in Pending_Approval
7. **You approve**: Move file to Approved folder
8. **You run**: `claude /approve-actions`
9. **Claude sends**: Email sent via Gmail API
10. **Logs action**: Updates Dashboard and moves to Done

### Example 2: LinkedIn Posting Flow

1. **Watcher suggests**: LinkedIn watcher creates posting reminder
2. **You run**: `claude /linkedin-post`
3. **Claude drafts**: Creates post based on Business_Goals.md
4. **Creates approval**: Draft in Pending_Approval folder
5. **You review**: Edit if needed, move to Approved
6. **You run**: `claude /approve-actions`
7. **Claude posts**: Uses Playwright to post on LinkedIn
8. **Logs action**: Updates Dashboard with post summary

### Example 3: WhatsApp Urgent Message

1. **Watcher detects**: WhatsApp message with "urgent invoice"
2. **Creates task**: `WHATSAPP_client_20260226.md` in Needs_Action
3. **You run**: `claude /process-tasks`
4. **Claude creates plan**: Multi-step plan for invoice handling
5. **Executes steps**: Generates invoice, drafts email
6. **Requests approval**: Email draft in Pending_Approval
7. **You approve**: Move to Approved
8. **Claude completes**: Sends email, logs action, updates Dashboard

## Approval Workflow

### How It Works

1. **Sensitive actions** (emails, posts, payments) create approval requests
2. **Files go to**: `/Pending_Approval/`
3. **You review**: Read the draft, edit if needed
4. **Approve**: Move to `/Approved/`
5. **Reject**: Move to `/Rejected/`
6. **Execute**: Run `/approve-actions` to process

### Approval File Format

```markdown
---
type: email|linkedin_post|payment
status: pending
created: 2026-02-26T10:00:00Z
expires: 2026-02-27T10:00:00Z
---

## Action Details
[What will be done]

## To Approve
Move this file to /Approved folder.

## To Reject
Move this file to /Rejected folder.
```

### Expiration

- Approvals expire after 24 hours
- Expired files moved to `/Expired/`
- Must create new approval request

## Scheduling

### Option 1: Cron (Mac/Linux)

```bash
# Edit crontab
crontab -e

# Add these lines:
# Process tasks every 30 minutes
*/30 * * * * cd /path/to/AI_Employee_Vault && claude /process-tasks

# Check for approvals every 15 minutes
*/15 * * * * cd /path/to/AI_Employee_Vault && claude /approve-actions

# Daily morning briefing at 8 AM
0 8 * * * cd /path/to/AI_Employee_Vault && claude /create-plan "task: daily briefing"
```

### Option 2: Task Scheduler (Windows)

1. Open Task Scheduler
2. Create Basic Task
3. Set trigger (e.g., every 30 minutes)
4. Action: Start a program
5. Program: `claude`
6. Arguments: `/process-tasks`
7. Start in: `D:\D drive Data\hacka0-silver\AI_Employee_Vault`

## Folder Structure

```
AI_Employee_Vault/
├── Dashboard.md
├── Company_Handbook.md
├── Business_Goals.md
├── Inbox/
├── Needs_Action/
│   ├── EMAIL_*.md
│   ├── WHATSAPP_*.md
│   └── LINKEDIN_*.md
├── Plans/
│   └── PLAN_*.md
├── Pending_Approval/
│   ├── EMAIL_*.md
│   └── LINKEDIN_POST_*.md
├── Approved/
├── Rejected/
├── Expired/
├── Done/
└── Logs/
    ├── 2026-02-26.json
    ├── gmail_watcher.log
    ├── whatsapp_watcher.log
    └── linkedin_watcher.log
```

## Testing Your Setup

### 1. Test Watchers

```bash
# Check watcher status
pm2 status

# View logs
pm2 logs gmail

# Send yourself a test email marked important
# Check if task appears in Needs_Action
```

### 2. Test Skills

```bash
# Create a test task manually
echo "Test task" > AI_Employee_Vault/Needs_Action/TEST_task.md

# Process it
claude /process-tasks

# Check Dashboard for updates
```

### 3. Test Approval Flow

```bash
# Create a test approval
claude /send-email "to: test@example.com, subject: Test"

# Check Pending_Approval folder
# Move to Approved
# Run approve-actions
claude /approve-actions
```

## Troubleshooting

### Watchers Not Creating Tasks

- Check watcher logs: `pm2 logs [watcher-name]`
- Verify vault path in watcher scripts
- Ensure Needs_Action folder exists
- Check state files aren't blocking

### Skills Not Working

- Verify skill files exist in `.claude/skills/`
- Check SKILL.md and prompt.md are present
- Run `claude --help` to see available skills
- Check Claude Code is in vault directory

### Approvals Not Executing

- Verify files are in `/Approved/` folder
- Check file format (YAML frontmatter)
- Ensure not expired
- Check logs for errors

### LinkedIn/WhatsApp Not Posting

- Verify Playwright MCP server running
- Check browser session is logged in
- Test with `/browsing-with-playwright` skill
- Review browser automation logs

## Security Checklist

- [ ] Gmail credentials in `.gitignore`
- [ ] Browser sessions in `.gitignore`
- [ ] Approval workflow tested
- [ ] Logs don't contain sensitive data
- [ ] State files backed up
- [ ] Watchers running as non-root user

## Next Steps to Gold Tier

After completing Silver Tier:
1. Add more MCP servers (calendar, payments)
2. Implement weekly business audit
3. Add Facebook/Instagram/Twitter integration
4. Set up Odoo accounting integration
5. Implement Ralph Wiggum loop for autonomy
6. Create comprehensive error recovery

## Silver Tier Completion Checklist

- [ ] Gmail watcher running continuously
- [ ] WhatsApp watcher detecting urgent messages
- [ ] LinkedIn watcher suggesting posts
- [ ] `/process-tasks` skill working
- [ ] `/create-plan` skill creating detailed plans
- [ ] `/send-email` skill with approval workflow
- [ ] `/linkedin-post` skill posting content
- [ ] `/approve-actions` skill executing approvals
- [ ] Scheduling configured (cron or Task Scheduler)
- [ ] End-to-end flow tested
- [ ] Documentation complete
- [ ] Demo video recorded

## Support

- Weekly Research Meeting: Wednesdays 10 PM
- Zoom: https://us06web.zoom.us/j/87188707642
- Submit Form: https://forms.gle/JR9T1SJq5rmQyGkGA

Congratulations on reaching Silver Tier! 🥈
