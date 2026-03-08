# Gmail Watcher - Quick Fix Guide

## Your Issue

```
ERROR - Credentials file not found: gmail_credentials.json
```

## Solution (5-10 minutes)

### Option 1: Full Gmail API Setup (Recommended for Reading Emails)

**Step 1: Run the setup helper**
```bash
cd D:\D drive Data\hacka0-silver\watchers
setup_gmail.bat
```

This will:
- Open Google Cloud Console in your browser
- Show you step-by-step instructions

**Step 2: Follow the on-screen instructions to:**
1. Create a Google Cloud project
2. Enable Gmail API
3. Create OAuth credentials (Desktop app)
4. Download the JSON file
5. Save it as: `D:\D drive Data\hacka0-silver\watchers\credentials\gmail_credentials.json`

**Step 3: Test your setup**
```bash
python test_gmail_credentials.py
```

**Step 4: Run the watcher**
```bash
python gmail_watcher.py
```

A browser will open for you to authorize access. After that, it will run automatically.

---

### Option 2: Skip Gmail Watcher (Quick Workaround)

If you don't want to set up Gmail API right now, you can:

**Just use WhatsApp and LinkedIn watchers instead:**
```bash
# Test WhatsApp watcher
python whatsapp_watcher.py

# Test LinkedIn watcher
python linkedin_watcher.py
```

**Or disable Gmail watcher in PM2:**
Edit `ecosystem.config.js` and comment out the gmail-watcher section.

---

### Option 3: Use SMTP Only (For Sending Emails Only)

If you only need to SEND emails (not read them):

1. Enable 2-factor authentication on Gmail
2. Generate App Password: https://myaccount.google.com/apppasswords
3. Create `.env` file:
   ```
   SMTP_USERNAME=your-email@gmail.com
   SMTP_PASSWORD=your-16-char-app-password
   ```
4. Use the `/send-email` skill (doesn't need Gmail API)

**Note:** SMTP can't read emails, only send them.

---

## Detailed Setup Instructions

See: `credentials/README.md`

## Test Your Setup

```bash
python test_gmail_credentials.py
```

This will check:
- [x] Credentials file exists
- [x] JSON format is valid
- [x] Python dependencies installed
- [x] Authentication token (after first run)

---

## Common Issues

### "Credentials file not found"
- Make sure the file is named exactly: `gmail_credentials.json`
- Make sure it's in the `credentials/` folder
- Check the full path matches what the error shows

### "Access blocked: This app's request is invalid"
- Add your email to "Test users" in OAuth consent screen
- Make sure app is in "Testing" mode (not "Production")

### "invalid_grant"
- Delete `gmail_token.json`
- Run `python gmail_watcher.py` again to re-authenticate

---

## Quick Links

- Google Cloud Console: https://console.cloud.google.com/
- Gmail API Quickstart: https://developers.google.com/gmail/api/quickstart/python
- App Passwords (for SMTP): https://myaccount.google.com/apppasswords

---

## Need Help?

1. Read: `credentials/README.md` (detailed guide)
2. Run: `python test_gmail_credentials.py` (diagnostic tool)
3. Check: Weekly meeting Wednesdays 10 PM (see main README)
