#!/usr/bin/env python3
"""
LinkedIn Watcher - Monitors LinkedIn for messages and engagement opportunities
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
SESSION_PATH = Path(__file__).parent / "sessions" / "linkedin"
CHECK_INTERVAL = 300  # seconds (5 minutes)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(VAULT_PATH / "Logs" / "linkedin_watcher.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("LinkedInWatcher")


class LinkedInWatcher:
    """Watches LinkedIn for messages and engagement opportunities"""

    def __init__(self, vault_path: Path, session_path: Path, check_interval: int = 300):
        self.vault_path = vault_path
        self.needs_action = vault_path / "Needs_Action"
        self.session_path = session_path
        self.check_interval = check_interval
        self.processed_messages: Set[str] = set()

        # Ensure directories exist
        self.needs_action.mkdir(parents=True, exist_ok=True)
        (vault_path / "Logs").mkdir(parents=True, exist_ok=True)
        self.session_path.mkdir(parents=True, exist_ok=True)

        # Load state
        self.state_file = vault_path / "Logs" / "linkedin_watcher_state.json"
        self._load_state()

    def _load_state(self):
        """Load previously processed message IDs"""
        if self.state_file.exists():
            try:
                with open(self.state_file, 'r') as f:
                    state = json.load(f)
                    self.processed_messages = set(state.get('processed_messages', []))
                logger.info(f"Loaded {len(self.processed_messages)} processed messages")
            except Exception as e:
                logger.error(f"Error loading state: {e}")

    def _save_state(self):
        """Save processed message IDs"""
        try:
            with open(self.state_file, 'w') as f:
                json.dump({
                    'processed_messages': list(self.processed_messages),
                    'last_updated': datetime.now().isoformat()
                }, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving state: {e}")

    def check_for_messages(self, page: Page) -> List[Dict]:
        """Check for new LinkedIn messages"""
        try:
            # Navigate to messaging
            page.goto('https://www.linkedin.com/messaging/')
            page.wait_for_load_state('networkidle')

            # Find unread conversations
            unread_convos = page.query_selector_all('.msg-conversation-listitem--unread')

            new_messages = []

            for convo in unread_convos[:5]:  # Check first 5 unread
                try:
                    # Get sender name
                    name_elem = convo.query_selector('.msg-conversation-listitem__participant-names')
                    name = name_elem.inner_text() if name_elem else "Unknown"

                    # Get message preview
                    preview_elem = convo.query_selector('.msg-conversation-listitem__message-snippet')
                    preview = preview_elem.inner_text() if preview_elem else ""

                    # Create unique ID
                    msg_id = f"{name}_{datetime.now().strftime('%Y%m%d')}"

                    if msg_id not in self.processed_messages:
                        new_messages.append({
                            'name': name,
                            'preview': preview[:200],
                            'msg_id': msg_id
                        })

                except Exception as e:
                    logger.error(f"Error processing conversation: {e}")
                    continue

            logger.info(f"Found {len(new_messages)} new LinkedIn messages")
            return new_messages

        except Exception as e:
            logger.error(f"Error checking LinkedIn messages: {e}")
            return []

    def check_for_posting_opportunity(self, page: Page) -> bool:
        """Check if it's time to post on LinkedIn"""
        try:
            # Read Dashboard to check last post date
            dashboard_path = self.vault_path / "Dashboard.md"
            if not dashboard_path.exists():
                return True  # No dashboard, suggest posting

            dashboard_content = dashboard_path.read_text()

            # Simple check: if "Posted on LinkedIn" not in recent activity today
            today = datetime.now().strftime('%Y-%m-%d')
            if f"[{today}" in dashboard_content and "Posted on LinkedIn" in dashboard_content:
                logger.info("Already posted on LinkedIn today")
                return False

            # Check posting schedule from Business_Goals
            business_goals_path = self.vault_path / "Business_Goals.md"
            if business_goals_path.exists():
                # Suggest posting if it's been more than 1 day
                return True

            return False

        except Exception as e:
            logger.error(f"Error checking posting opportunity: {e}")
            return False

    def create_message_action_file(self, message: Dict) -> Path:
        """Create action file for new LinkedIn message"""
        try:
            content = f"""---
type: linkedin_message
from: {message['name']}
received: {datetime.now().isoformat()}
msg_id: {message['msg_id']}
priority: normal
status: pending
---

## LinkedIn Message

**From:** {message['name']}
**Received:** {datetime.now().strftime('%Y-%m-%d %H:%M')}

## Message Preview

{message['preview']}

## Suggested Actions

- [ ] Read full message on LinkedIn
- [ ] Assess if this is a sales lead or networking opportunity
- [ ] Draft appropriate response
- [ ] Request approval if needed
- [ ] Send response via LinkedIn

## Notes

Review the sender's profile to understand context and intent.
"""

            # Create filename
            safe_name = "".join(c for c in message['name'] if c.isalnum() or c in (' ', '-', '_'))[:30]
            filename = f"LINKEDIN_MSG_{safe_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
            filepath = self.needs_action / filename

            # Write file
            filepath.write_text(content, encoding='utf-8')

            # Mark as processed
            self.processed_messages.add(message['msg_id'])
            self._save_state()

            logger.info(f"Created action file: {filename}")
            return filepath

        except Exception as e:
            logger.error(f"Error creating action file: {e}")
            return None

    def create_posting_reminder(self) -> Path:
        """Create reminder to post on LinkedIn"""
        try:
            content = f"""---
type: linkedin_post_reminder
created: {datetime.now().isoformat()}
priority: normal
status: pending
---

## LinkedIn Posting Reminder

It's time to post on LinkedIn to generate business leads.

## Suggested Actions

- [ ] Run `/linkedin-post` skill to draft a post
- [ ] Review and approve the draft
- [ ] Post will be published automatically after approval

## Posting Strategy

- Focus on business value and insights
- Share client success stories (with permission)
- Provide tips related to your services
- Include clear call-to-action
- Use 3-5 relevant hashtags

## Notes

Regular posting (3-5x per week) helps maintain visibility and generate leads.
"""

            filename = f"LINKEDIN_POST_REMINDER_{datetime.now().strftime('%Y%m%d')}.md"
            filepath = self.needs_action / filename

            # Write file
            filepath.write_text(content, encoding='utf-8')

            logger.info(f"Created posting reminder: {filename}")
            return filepath

        except Exception as e:
            logger.error(f"Error creating posting reminder: {e}")
            return None

    def run(self):
        """Main watcher loop"""
        logger.info(f"Starting LinkedIn Watcher (checking every {self.check_interval}s)")
        logger.info(f"Vault path: {self.vault_path}")
        logger.info(f"Session path: {self.session_path}")

        with sync_playwright() as p:
            # Launch browser with persistent context
            browser = p.chromium.launch_persistent_context(
                str(self.session_path),
                headless=False,  # Set to True for production
                args=['--no-sandbox']
            )

            page = browser.pages[0] if browser.pages else browser.new_page()

            # Navigate to LinkedIn
            logger.info("Navigating to LinkedIn...")
            page.goto('https://www.linkedin.com')

            # Wait for user to log in if needed
            logger.info("Waiting for LinkedIn to load (log in if needed)...")
            try:
                page.wait_for_selector('[data-test-global-nav-search]', timeout=60000)
                logger.info("LinkedIn loaded successfully")
            except Exception as e:
                logger.error("Failed to load LinkedIn. Please log in.")
                browser.close()
                return

            # Main loop
            while True:
                try:
                    # Check for new messages
                    messages = self.check_for_messages(page)

                    # Create action files for messages
                    for msg in messages:
                        self.create_message_action_file(msg)

                    # Check if posting opportunity exists
                    if self.check_for_posting_opportunity(page):
                        self.create_posting_reminder()

                    # Wait before next check
                    time.sleep(self.check_interval)

                except KeyboardInterrupt:
                    logger.info("LinkedIn Watcher stopped by user")
                    break
                except Exception as e:
                    logger.error(f"Error in main loop: {e}")
                    time.sleep(self.check_interval)

            browser.close()


def main():
    """Entry point"""
    watcher = LinkedInWatcher(VAULT_PATH, SESSION_PATH, CHECK_INTERVAL)
    watcher.run()


if __name__ == "__main__":
    main()
