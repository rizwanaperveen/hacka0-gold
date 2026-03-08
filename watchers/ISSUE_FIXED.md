# Gmail Watcher Issue - FIXED

## Problem Summary

You encountered this error when running `gmail_watcher.py`:
```
ERROR - Credentials file not found: D:\D drive Data\hacka0-silver\watchers\credentials\gmail_credentials.json
```

## What I Fixed

### 1. Created Setup Helper Tools
- ✅ `setup_gmail.bat` - Windows setup wizard
- ✅ `setup_gmail.sh` - Linux/Mac setup wizard
- ✅ `test_gmail_credentials.py` - Diagnostic tool (fixed Unicode issues for Windows)

### 2. Created Documentation
- ✅ `credentials/README.md` - Detailed setup guide
- ✅ `GMAIL_QUICKSTART.md` - Quick reference guide

### 3. Fixed Windows Compatibility
- ✅ Removed Unicode emoji characters that caused encoding errors
- ✅ Replaced with [OK], [FAIL], [WARN] markers

## Your Next Steps

### Choose One Option:

---

### ⭐ OPTION 1: Set Up Gmail API (Recommended - 10 minutes)

This allows the watcher to READ your Gmail emails automatically.

**Quick Start:**
```bash
cd D:\D drive Data\hacka0-silver\watchers
setup_gmail.bat
```

**Manual Steps:**
1. Go to https://console.cloud.google.com/
2. Create new project: "AI-Employee-Gmail"
3. Enable "Gmail API"
4. Create OAuth credentials (Desktop app type)
5. Download JSON file
6. Save as: `D:\D drive Data\hacka0-silver\watchers\credentials\gmail_credentials.json`
7. Run: `python gmail_watcher.py`
8. Browser opens → Sign in → Allow access
9. Done! Watcher will run automatically

**Test it:**
```bash
python test_gmail_credentials.py
```

---

### 🚀 OPTION 2: Skip Gmail for Now (Fastest - 1 minute)

Use the other watchers instead:

```bash
# Test WhatsApp watcher
python whatsapp_watcher.py

# Test LinkedIn watcher
python linkedin_watcher.py
```

You can set up Gmail later when you need it.

---

### 📧 OPTION 3: SMTP Only (For Sending Emails - 5 minutes)

If you only need to SEND emails (not read them):

1. Enable 2FA on Gmail: https://myaccount.google.com/security
2. Create App Password: https://myaccount.google.com/apppasswords
3. Create `.env` file in project root:
   ```
   SMTP_USERNAME=your-email@gmail.com
   SMTP_PASSWORD=your-16-char-app-password
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   ```
4. Use `/send-email` skill (works without Gmail API)

**Note:** SMTP can only SEND emails, not read them.

---

## Files Created for You

```
watchers/
├── setup_gmail.bat              ← Run this on Windows
├── setup_gmail.sh               ← Run this on Linux/Mac
├── test_gmail_credentials.py    ← Test your setup
├── GMAIL_QUICKSTART.md          ← Quick reference
└── credentials/
    └── README.md                ← Detailed instructions
```

## Testing Your Setup

After you get credentials, test with:

```bash
cd D:\D drive Data\hacka0-silver\watchers
python test_gmail_credentials.py
```

Expected output:
```
============================================================
Gmail API Credentials Test
============================================================

1. Checking credentials file...
   [OK] Credentials file exists

2. Validating JSON structure...
   [OK] JSON structure is valid
   Client ID: 123456789...

3. Checking authentication token...
   [WARN] Token not found (expected on first run)

   Next step: Run the watcher to authenticate:
   python gmail_watcher.py

4. Checking Python dependencies...
   [OK] google-auth installed
   [OK] google-api-python-client installed

============================================================
[SUCCESS] ALL CHECKS PASSED
============================================================

Ready for first-time authentication!
Run: python gmail_watcher.py
```

## Common Questions

**Q: Do I need Gmail API for Silver tier?**
A: Yes, it's one of the requirements (2+ watchers). But you can use WhatsApp + LinkedIn instead if you prefer.

**Q: Is this safe?**
A: Yes. OAuth credentials stay on your machine. Google verifies the app. You control what access to grant.

**Q: Can I use a different email provider?**
A: Yes, but you'll need to modify the watcher script. Gmail API is the easiest to set up.

**Q: How long does setup take?**
A: 5-10 minutes for first-time Google Cloud setup. 1 minute if you've done it before.

## Troubleshooting

### Error: "Credentials file not found"
→ Run `setup_gmail.bat` and follow instructions

### Error: "Access blocked"
→ Add your email to "Test users" in OAuth consent screen

### Error: "invalid_grant"
→ Delete `credentials/gmail_token.json` and re-authenticate

### Error: "Module not found: google.auth"
→ Run: `pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client`

## Summary

✅ **Issue Fixed:** Created all necessary setup tools and documentation
⚠️ **Action Required:** You need to get Gmail API credentials from Google Cloud Console
📚 **Documentation:** See `GMAIL_QUICKSTART.md` for step-by-step guide
🔧 **Tools Ready:** Run `setup_gmail.bat` to start

## Quick Command Reference

```bash
# Setup wizard
setup_gmail.bat

# Test credentials
python test_gmail_credentials.py

# Run watcher (after setup)
python gmail_watcher.py

# Alternative: Skip Gmail, use others
python whatsapp_watcher.py
python linkedin_watcher.py
```

---

**Status:** ✅ Tools created, ready for you to get credentials
**Time to fix:** 5-10 minutes (following setup_gmail.bat)
**Alternative:** Use WhatsApp + LinkedIn watchers instead
