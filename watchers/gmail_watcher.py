#!/usr/bin/env python3
"""
Gmail Watcher - Monitors Gmail for important unread messages
Part of the AI Employee Silver Tier implementation
"""

import os
import sys
import time
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Set
import json

# Gmail API imports
try:
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
    import pickle
except ImportError:
    print("Error: Gmail API libraries not installed.")
    print("Install with: pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client")
    sys.exit(1)

# Configuration
VAULT_PATH = Path(__file__).parent.parent  # watchers/ -> AI_Employee_Vault/
NEEDS_ACTION = VAULT_PATH / "Needs_Action"
CREDENTIALS_PATH = Path(__file__).parent / "credentials" / "gmail_credentials.json"
TOKEN_PATH = Path(__file__).parent / "credentials" / "gmail_token.pickle"
CHECK_INTERVAL = 120  # seconds (2 minutes)
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(VAULT_PATH / "Logs" / "gmail_watcher.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("GmailWatcher")


class GmailWatcher:
    """Watches Gmail for important unread messages and creates action items"""

    def __init__(self, vault_path: Path, check_interval: int = 120):
        self.vault_path = vault_path
        self.needs_action = vault_path / "Needs_Action"
        self.check_interval = check_interval
        self.processed_ids: Set[str] = set()
        self.service = None

        # Ensure directories exist
        self.needs_action.mkdir(parents=True, exist_ok=True)
        (vault_path / "Logs").mkdir(parents=True, exist_ok=True)

        # Load processed IDs from state file
        self.state_file = vault_path / "Logs" / "gmail_watcher_state.json"
        self._load_state()

    def _load_state(self):
        """Load previously processed message IDs"""
        if self.state_file.exists():
            try:
                with open(self.state_file, 'r') as f:
                    state = json.load(f)
                    self.processed_ids = set(state.get('processed_ids', []))
                logger.info(f"Loaded {len(self.processed_ids)} processed message IDs")
            except Exception as e:
                logger.error(f"Error loading state: {e}")

    def _save_state(self):
        """Save processed message IDs"""
        try:
            with open(self.state_file, 'w') as f:
                json.dump({
                    'processed_ids': list(self.processed_ids),
                    'last_updated': datetime.now().isoformat()
                }, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving state: {e}")

    def authenticate(self):
        """Authenticate with Gmail API"""
        creds = None

        # Load existing token
        if TOKEN_PATH.exists():
            with open(TOKEN_PATH, 'rb') as token:
                creds = pickle.load(token)

        # If no valid credentials, authenticate
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not CREDENTIALS_PATH.exists():
                    logger.error(f"Credentials file not found: {CREDENTIALS_PATH}")
                    logger.error("Download credentials from Google Cloud Console")
                    sys.exit(1)

                flow = InstalledAppFlow.from_client_secrets_file(
                    str(CREDENTIALS_PATH), SCOPES)
                creds = flow.run_local_server(port=0)

            # Save credentials
            TOKEN_PATH.parent.mkdir(parents=True, exist_ok=True)
            with open(TOKEN_PATH, 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('gmail', 'v1', credentials=creds)
        logger.info("Gmail authentication successful")

    def check_for_updates(self) -> List[Dict]:
        """Check for new important unread messages"""
        try:
            # Query for unread important messages
            results = self.service.users().messages().list(
                userId='me',
                q='is:unread is:important',
                maxResults=10
            ).execute()

            messages = results.get('messages', [])

            # Filter out already processed messages
            new_messages = [
                msg for msg in messages
                if msg['id'] not in self.processed_ids
            ]

            logger.info(f"Found {len(new_messages)} new important messages")
            return new_messages

        except Exception as e:
            logger.error(f"Error checking Gmail: {e}")
            return []

    def create_action_file(self, message: Dict) -> Path:
        """Create action file for a new message"""
        try:
            # Get full message details
            msg = self.service.users().messages().get(
                userId='me',
                id=message['id'],
                format='full'
            ).execute()

            # Extract headers
            headers = {
                h['name']: h['value']
                for h in msg['payload']['headers']
            }

            from_email = headers.get('From', 'Unknown')
            subject = headers.get('Subject', 'No Subject')
            date = headers.get('Date', '')

            # Get message snippet
            snippet = msg.get('snippet', '')

            # Create action file
            content = f"""---
type: email
from: {from_email}
subject: {subject}
received: {datetime.now().isoformat()}
gmail_id: {message['id']}
priority: high
status: pending
---

## Email Details

**From:** {from_email}
**Subject:** {subject}
**Date:** {date}

## Message Preview

{snippet}

## Suggested Actions

- [ ] Read full email and assess urgency
- [ ] Draft appropriate response
- [ ] Request approval if needed
- [ ] Send response
- [ ] Archive or file

## Notes

[Add any context or notes here]
"""

            # Create filename
            safe_subject = "".join(c for c in subject if c.isalnum() or c in (' ', '-', '_'))[:50]
            filename = f"EMAIL_{safe_subject}_{message['id'][:8]}.md"
            filepath = self.needs_action / filename

            # Write file
            filepath.write_text(content, encoding='utf-8')

            # Mark as processed
            self.processed_ids.add(message['id'])
            self._save_state()

            logger.info(f"Created action file: {filename}")
            return filepath

        except Exception as e:
            logger.error(f"Error creating action file: {e}")
            return None

    def run(self):
        """Main watcher loop"""
        logger.info(f"Starting Gmail Watcher (checking every {self.check_interval}s)")
        logger.info(f"Vault path: {self.vault_path}")

        # Authenticate
        self.authenticate()

        while True:
            try:
                # Check for new messages
                messages = self.check_for_updates()

                # Create action files
                for msg in messages:
                    self.create_action_file(msg)

                # Wait before next check
                time.sleep(self.check_interval)

            except KeyboardInterrupt:
                logger.info("Gmail Watcher stopped by user")
                break
            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                time.sleep(self.check_interval)


def main():
    """Entry point"""
    watcher = GmailWatcher(VAULT_PATH, CHECK_INTERVAL)
    watcher.run()


if __name__ == "__main__":
    main()
