#!/usr/bin/env python3
"""
WhatsApp Watcher - Monitors WhatsApp Web for urgent messages
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

# Playwright imports
try:
    from playwright.sync_api import sync_playwright, Browser, Page
except ImportError:
    print("Error: Playwright not installed.")
    print("Install with: pip install playwright && playwright install chromium")
    sys.exit(1)

# Configuration
VAULT_PATH = Path(__file__).parent.parent / "AI_Employee_Vault"
NEEDS_ACTION = VAULT_PATH / "Needs_Action"
SESSION_PATH = Path(__file__).parent / "sessions" / "whatsapp"
CHECK_INTERVAL = 30  # seconds
URGENT_KEYWORDS = ['urgent', 'asap', 'emergency', 'help', 'invoice', 'payment', 'important']

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(VAULT_PATH / "Logs" / "whatsapp_watcher.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("WhatsAppWatcher")


class WhatsAppWatcher:
    """Watches WhatsApp Web for urgent messages and creates action items"""

    def __init__(self, vault_path: Path, session_path: Path, check_interval: int = 30):
        self.vault_path = vault_path
        self.needs_action = vault_path / "Needs_Action"
        self.session_path = session_path
        self.check_interval = check_interval
        self.processed_chats: Set[str] = set()
        self.keywords = URGENT_KEYWORDS

        # Ensure directories exist
        self.needs_action.mkdir(parents=True, exist_ok=True)
        (vault_path / "Logs").mkdir(parents=True, exist_ok=True)
        self.session_path.mkdir(parents=True, exist_ok=True)

        # Load state
        self.state_file = vault_path / "Logs" / "whatsapp_watcher_state.json"
        self._load_state()

    def _load_state(self):
        """Load previously processed chat IDs"""
        if self.state_file.exists():
            try:
                with open(self.state_file, 'r') as f:
                    state = json.load(f)
                    self.processed_chats = set(state.get('processed_chats', []))
                logger.info(f"Loaded {len(self.processed_chats)} processed chats")
            except Exception as e:
                logger.error(f"Error loading state: {e}")

    def _save_state(self):
        """Save processed chat IDs"""
        try:
            with open(self.state_file, 'w') as f:
                json.dump({
                    'processed_chats': list(self.processed_chats),
                    'last_updated': datetime.now().isoformat()
                }, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving state: {e}")

    def check_for_updates(self, page: Page) -> List[Dict]:
        """Check for new urgent messages"""
        try:
            # Wait for chat list to load
            page.wait_for_selector('[data-testid="chat-list"]', timeout=10000)

            # Find unread chats
            unread_chats = page.query_selector_all('[aria-label*="unread"]')

            urgent_messages = []

            for chat in unread_chats[:5]:  # Check first 5 unread chats
                try:
                    # Get chat text
                    text = chat.inner_text().lower()

                    # Check for urgent keywords
                    if any(keyword in text for keyword in self.keywords):
                        # Get chat name
                        name_elem = chat.query_selector('[dir="auto"]')
                        name = name_elem.inner_text() if name_elem else "Unknown"

                        # Create unique ID
                        chat_id = f"{name}_{datetime.now().strftime('%Y%m%d')}"

                        if chat_id not in self.processed_chats:
                            urgent_messages.append({
                                'name': name,
                                'text': text[:200],  # First 200 chars
                                'chat_id': chat_id
                            })

                except Exception as e:
                    logger.error(f"Error processing chat: {e}")
                    continue

            logger.info(f"Found {len(urgent_messages)} urgent messages")
            return urgent_messages

        except Exception as e:
            logger.error(f"Error checking WhatsApp: {e}")
            return []

    def create_action_file(self, message: Dict) -> Path:
        """Create action file for urgent message"""
        try:
            content = f"""---
type: whatsapp
from: {message['name']}
received: {datetime.now().isoformat()}
chat_id: {message['chat_id']}
priority: high
status: pending
---

## WhatsApp Message

**From:** {message['name']}
**Received:** {datetime.now().strftime('%Y-%m-%d %H:%M')}

## Message Preview

{message['text']}

## Suggested Actions

- [ ] Read full conversation in WhatsApp
- [ ] Assess urgency and required response
- [ ] Draft response
- [ ] Request approval if needed
- [ ] Send response via WhatsApp

## Notes

This message was flagged as urgent based on keywords.
Review the full conversation for context.
"""

            # Create filename
            safe_name = "".join(c for c in message['name'] if c.isalnum() or c in (' ', '-', '_'))[:30]
            filename = f"WHATSAPP_{safe_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
            filepath = self.needs_action / filename

            # Write file
            filepath.write_text(content, encoding='utf-8')

            # Mark as processed
            self.processed_chats.add(message['chat_id'])
            self._save_state()

            logger.info(f"Created action file: {filename}")
            return filepath

        except Exception as e:
            logger.error(f"Error creating action file: {e}")
            return None

    def run(self):
        """Main watcher loop"""
        logger.info(f"Starting WhatsApp Watcher (checking every {self.check_interval}s)")
        logger.info(f"Vault path: {self.vault_path}")
        logger.info(f"Session path: {self.session_path}")

        with sync_playwright() as p:
            # Launch browser with persistent context (saves login)
            browser = p.chromium.launch_persistent_context(
                str(self.session_path),
                headless=False,  # Set to True for production
                args=['--no-sandbox']
            )

            page = browser.pages[0] if browser.pages else browser.new_page()

            # Navigate to WhatsApp Web
            logger.info("Navigating to WhatsApp Web...")
            page.goto('https://web.whatsapp.com')

            # Wait for user to scan QR code if needed
            logger.info("Waiting for WhatsApp to load (scan QR if needed)...")
            try:
                page.wait_for_selector('[data-testid="chat-list"]', timeout=60000)
                logger.info("WhatsApp loaded successfully")
            except Exception as e:
                logger.error("Failed to load WhatsApp. Please scan QR code.")
                browser.close()
                return

            # Main loop
            while True:
                try:
                    # Check for urgent messages
                    messages = self.check_for_updates(page)

                    # Create action files
                    for msg in messages:
                        self.create_action_file(msg)

                    # Wait before next check
                    time.sleep(self.check_interval)

                except KeyboardInterrupt:
                    logger.info("WhatsApp Watcher stopped by user")
                    break
                except Exception as e:
                    logger.error(f"Error in main loop: {e}")
                    time.sleep(self.check_interval)

            browser.close()


def main():
    """Entry point"""
    watcher = WhatsAppWatcher(VAULT_PATH, SESSION_PATH, CHECK_INTERVAL)
    watcher.run()


if __name__ == "__main__":
    main()
