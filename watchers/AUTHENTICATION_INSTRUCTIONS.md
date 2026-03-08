# Gmail Watcher - Authentication Instructions

## ✅ Good News: Your Gmail Watcher is Running!

The watcher started successfully and is now waiting for you to authenticate.

## What's Happening Now

The Gmail watcher is waiting at the OAuth authentication step. A browser window **should have opened** automatically with a Google sign-in page.

## If Browser Opened

1. **Sign in** with your Gmail account
2. **Click "Allow"** to grant access to read your emails
3. The browser will show "The authentication flow has completed"
4. Return to your terminal - the watcher will continue automatically

## If Browser Did NOT Open

The authentication URL might be in your terminal. Look for a message like:
```
Please visit this URL to authorize this application:
https://accounts.google.com/o/oauth2/auth?...
```

Copy that URL and paste it into your browser manually.

## Current Status

```
✅ Credentials file found
✅ Watcher started
⏳ Waiting for OAuth authentication
```

## Next Steps

### Option 1: Run Interactively (Recommended)

Open a **new terminal window** and run:

```bash
cd "D:\D drive Data\hacka0-silver\AI_Employee_Vault\watchers"
python gmail_watcher.py
```

This will:
- Open a browser automatically
- Show you the authentication URL if browser fails
- Let you see the authentication process

### Option 2: Check if Browser Already Opened

Look for a browser window/tab that opened with:
- URL starting with `accounts.google.com`
- Title like "Sign in - Google Accounts"
- Asking you to choose your Gmail account

### Option 3: Manual Authentication

If you see an authentication URL in the terminal output, copy it and:
1. Paste into your browser
2. Sign in with Gmail
3. Click "Allow"
4. Return to terminal

## After Authentication

Once you complete authentication:
- A `gmail_token.pickle` file will be created
- The watcher will start monitoring your Gmail
- You'll see log messages like "Gmail authentication successful"
- Future runs won't need authentication (token is saved)

## Troubleshooting

### "Access blocked: This app's request is invalid"
- Go to Google Cloud Console
- OAuth consent screen → Add your email to "Test users"

### "Redirect URI mismatch"
- Your credentials are configured correctly (Desktop app)
- This shouldn't happen

### Browser doesn't open
- Check if port 8080 or similar is blocked
- Try running as administrator
- Look for the authentication URL in terminal output

---

**What to do RIGHT NOW:**

1. Check if a browser window opened
2. If yes → Sign in and click "Allow"
3. If no → Run `python gmail_watcher.py` in a new terminal window
4. Complete the authentication
5. Come back and tell me if it worked!
