# AI Employee Watchers - Silver Tier

Automated monitoring scripts that watch external services and create action items in your AI Employee vault.

## Overview

Watchers are lightweight Python scripts that run continuously in the background, monitoring:
- **Gmail**: Important unread emails
- **WhatsApp**: Urgent messages with keywords
- **LinkedIn**: New messages and posting opportunities

When they detect something requiring attention, they create task files in `/Needs_Action/` for Claude to process.

## Setup

### 1. Install Dependencies

```bash
cd watchers
pip install -r requirements.txt
```

For Playwright (WhatsApp & LinkedIn):
```bash
playwright install chromium
```

### 2. Configure Gmail Watcher

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable Gmail API
4. Create OAuth 2.0 credentials (Desktop app)
5. Download credentials JSON
6. Save as `watchers/credentials/gmail_credentials.json`

First run will open browser for authentication:
```bash
python gmail_watcher.py
```

### 3. Configure WhatsApp Watcher

WhatsApp uses browser automation with session persistence:

```bash
python whatsapp_watcher.py
```

On first run:
1. Browser opens to WhatsApp Web
2. Scan QR code with your phone
3. Session is saved for future runs

### 4. Configure LinkedIn Watcher

Similar to WhatsApp:

```bash
python linkedin_watcher.py
```

On first run:
1. Browser opens to LinkedIn
2. Log in with your credentials
3. Session is saved for future runs

## Running Watchers

### Manual Start

```bash
# Start each watcher in separate terminal
python gmail_watcher.py
python whatsapp_watcher.py
python linkedin_watcher.py
```

### Background Mode (Recommended)

Using PM2 (Node.js process manager):

```bash
# Install PM2
npm install -g pm2

# Start all watchers
pm2 start gmail_watcher.py --interpreter python3 --name gmail-watcher
pm2 start whatsapp_watcher.py --interpreter python3 --name whatsapp-watcher
pm2 start linkedin_watcher.py --interpreter python3 --name linkedin-watcher

# Save configuration
pm2 save

# Setup auto-start on boot
pm2 startup
```

### Check Status

```bash
pm2 status
pm2 logs gmail-watcher
```

### Stop Watchers

```bash
pm2 stop all
# or
pm2 stop gmail-watcher
```

## How Watchers Work

### Gmail Watcher

- **Checks**: Every 2 minutes
- **Monitors**: Unread emails marked as "important"
- **Creates**: `EMAIL_[subject]_[id].md` in Needs_Action
- **State**: Tracks processed message IDs to avoid duplicates

### WhatsApp Watcher

- **Checks**: Every 30 seconds
- **Monitors**: Unread chats containing urgent keywords
- **Keywords**: urgent, asap, emergency, help, invoice, payment, important
- **Creates**: `WHATSAPP_[sender]_[timestamp].md` in Needs_Action
- **State**: Tracks processed chats by date

### LinkedIn Watcher

- **Checks**: Every 5 minutes
- **Monitors**:
  - New unread messages
  - Posting opportunities (daily schedule)
- **Creates**:
  - `LINKEDIN_MSG_[sender]_[timestamp].md` for messages
  - `LINKEDIN_POST_REMINDER_[date].md` for posting
- **State**: Tracks processed messages

## Configuration

### Adjust Check Intervals

Edit the watcher files:

```python
# In gmail_watcher.py
CHECK_INTERVAL = 120  # seconds (2 minutes)

# In whatsapp_watcher.py
CHECK_INTERVAL = 30  # seconds

# In linkedin_watcher.py
CHECK_INTERVAL = 300  # seconds (5 minutes)
```

### Customize Keywords (WhatsApp)

```python
# In whatsapp_watcher.py
URGENT_KEYWORDS = ['urgent', 'asap', 'emergency', 'help', 'invoice', 'payment', 'important']
```

### Change Vault Path

```python
# In any watcher file
VAULT_PATH = Path("/path/to/your/AI_Employee_Vault")
```

## Logs

All watchers log to:
- Console (stdout)
- `AI_Employee_Vault/Logs/[watcher]_watcher.log`

View logs:
```bash
tail -f ../AI_Employee_Vault/Logs/gmail_watcher.log
```

## State Files

Watchers maintain state to avoid processing duplicates:
- `AI_Employee_Vault/Logs/gmail_watcher_state.json`
- `AI_Employee_Vault/Logs/whatsapp_watcher_state.json`
- `AI_Employee_Vault/Logs/linkedin_watcher_state.json`

To reset (reprocess all messages):
```bash
rm ../AI_Employee_Vault/Logs/*_watcher_state.json
```

## Troubleshooting

### Gmail: 403 Forbidden
- Enable Gmail API in Google Cloud Console
- Verify OAuth consent screen is configured
- Check credentials file path

### WhatsApp: QR Code Not Appearing
- Ensure browser is not headless (set `headless=False`)
- Clear session: `rm -rf sessions/whatsapp`
- Try again

### LinkedIn: Login Required Every Time
- Session not persisting
- Check `sessions/linkedin` directory permissions
- Ensure browser context is persistent

### Watcher Stops Running
- Use PM2 or similar process manager
- Check logs for errors
- Implement watchdog script (see main hackathon doc)

## Security Notes

- **Credentials**: Never commit `credentials/` folder to git
- **Sessions**: Browser sessions contain auth tokens, keep secure
- **Logs**: May contain message previews, review before sharing
- **State Files**: Safe to commit, contain only IDs

## Integration with AI Employee

Once watchers create files in `/Needs_Action/`:

1. Run `/process-tasks` skill in Claude Code
2. Claude reads the task files
3. Creates plans if needed
4. Executes or requests approval
5. Moves completed tasks to `/Done/`

## Next Steps

After setting up watchers:
1. Configure MCP servers for actions (email sending, etc.)
2. Set up approval workflow
3. Test end-to-end flow
4. Schedule regular `/process-tasks` runs
5. Implement Ralph Wiggum loop for autonomous operation

## Silver Tier Checklist

- [ ] Gmail watcher running and creating tasks
- [ ] WhatsApp watcher running and detecting urgent messages
- [ ] LinkedIn watcher running and suggesting posts
- [ ] All watchers logging properly
- [ ] State persistence working
- [ ] Process manager configured (PM2)
- [ ] Integration with Claude Code tested
