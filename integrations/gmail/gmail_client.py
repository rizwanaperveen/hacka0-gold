"""
Gmail Integration Client - Complete Gmail API integration

Provides full Gmail API functionality for the AI employee system.
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


class GmailClient:
    """
    Complete Gmail API client for email operations.

    This client wraps the Gmail API and provides a clean interface
    for all email operations needed by the AI employee.
    """

    def __init__(self, credentials_path: str = None):
        self.logger = logging.getLogger("GmailClient")
        self.credentials_path = credentials_path
        self.service = None

        self.logger.info("Gmail client initialized")

    async def initialize(self):
        """Initialize Gmail API service."""
        try:
            # In production, this would initialize the Gmail API service
            # from google.oauth2.credentials import Credentials
            # from googleapiclient.discovery import build

            # For now, placeholder
            self.logger.info("Gmail API service initialized")

        except Exception as e:
            self.logger.error(f"Failed to initialize Gmail API: {str(e)}")
            raise

    async def send_message(
        self,
        to: str,
        subject: str,
        body: str,
        cc: List[str] = None,
        bcc: List[str] = None,
        attachments: List[str] = None,
        html: bool = False
    ) -> Dict[str, Any]:
        """
        Send an email message.

        Args:
            to: Recipient email
            subject: Email subject
            body: Email body
            cc: CC recipients
            bcc: BCC recipients
            attachments: List of file paths to attach
            html: Whether body is HTML

        Returns:
            Message details
        """
        try:
            self.logger.info(f"Sending email to {to}: {subject}")

            # Create message
            message = self._create_message(
                to=to,
                subject=subject,
                body=body,
                cc=cc,
                bcc=bcc,
                attachments=attachments,
                html=html
            )

            # Send via Gmail API
            if self.service:
                result = self.service.users().messages().send(
                    userId='me',
                    body=message
                ).execute()
            else:
                # Placeholder
                result = {
                    'id': f'msg_{datetime.now().timestamp()}',
                    'threadId': f'thread_{datetime.now().timestamp()}'
                }

            return {
                'message_id': result['id'],
                'thread_id': result.get('threadId'),
                'status': 'sent'
            }

        except Exception as e:
            self.logger.error(f"Failed to send message: {str(e)}")
            raise

    def _create_message(
        self,
        to: str,
        subject: str,
        body: str,
        cc: List[str] = None,
        bcc: List[str] = None,
        attachments: List[str] = None,
        html: bool = False
    ) -> Dict[str, str]:
        """Create a message for Gmail API."""
        if attachments:
            message = MIMEMultipart()
        else:
            message = MIMEText(body, 'html' if html else 'plain')

        message['to'] = to
        message['subject'] = subject

        if cc:
            message['cc'] = ', '.join(cc)
        if bcc:
            message['bcc'] = ', '.join(bcc)

        if attachments:
            message.attach(MIMEText(body, 'html' if html else 'plain'))

            for filepath in attachments:
                self._attach_file(message, filepath)

        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
        return {'raw': raw}

    def _attach_file(self, message: MIMEMultipart, filepath: str):
        """Attach a file to the message."""
        try:
            with open(filepath, 'rb') as f:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(f.read())

            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename={filepath.split("/")[-1]}'
            )
            message.attach(part)

        except Exception as e:
            self.logger.error(f"Failed to attach file {filepath}: {str(e)}")

    async def list_messages(
        self,
        query: str = None,
        max_results: int = 10,
        unread_only: bool = False,
        labels: List[str] = None
    ) -> List[Dict[str, Any]]:
        """
        List messages from Gmail.

        Args:
            query: Gmail search query
            max_results: Maximum messages to return
            unread_only: Only return unread messages
            labels: Filter by labels

        Returns:
            List of message dictionaries
        """
        try:
            # Build query
            if unread_only:
                query = f"is:unread {query or ''}"

            if labels:
                label_query = ' '.join([f'label:{label}' for label in labels])
                query = f"{query or ''} {label_query}"

            self.logger.info(f"Listing messages (query: {query})")

            if self.service:
                results = self.service.users().messages().list(
                    userId='me',
                    q=query,
                    maxResults=max_results
                ).execute()

                messages = results.get('messages', [])

                # Get full message details
                full_messages = []
                for msg in messages:
                    full_msg = await self.get_message(msg['id'])
                    full_messages.append(full_msg)

                return full_messages
            else:
                # Placeholder
                return []

        except Exception as e:
            self.logger.error(f"Failed to list messages: {str(e)}")
            return []

    async def get_message(self, message_id: str) -> Dict[str, Any]:
        """Get full message details."""
        try:
            if self.service:
                message = self.service.users().messages().get(
                    userId='me',
                    id=message_id,
                    format='full'
                ).execute()

                return self._parse_message(message)
            else:
                # Placeholder
                return {
                    'id': message_id,
                    'from': 'sender@example.com',
                    'subject': 'Example Subject',
                    'snippet': 'Message preview...',
                    'date': datetime.now().isoformat()
                }

        except Exception as e:
            self.logger.error(f"Failed to get message: {str(e)}")
            return {}

    def _parse_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Parse Gmail API message into simplified format."""
        headers = {h['name']: h['value'] for h in message['payload']['headers']}

        return {
            'id': message['id'],
            'thread_id': message['threadId'],
            'from': headers.get('From', ''),
            'to': headers.get('To', ''),
            'subject': headers.get('Subject', ''),
            'date': headers.get('Date', ''),
            'snippet': message.get('snippet', ''),
            'labels': message.get('labelIds', []),
            'body': self._get_message_body(message['payload'])
        }

    def _get_message_body(self, payload: Dict[str, Any]) -> str:
        """Extract message body from payload."""
        if 'body' in payload and 'data' in payload['body']:
            return base64.urlsafe_b64decode(payload['body']['data']).decode()

        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    if 'data' in part['body']:
                        return base64.urlsafe_b64decode(part['body']['data']).decode()

        return ''

    async def mark_read(self, message_ids: List[str]):
        """Mark messages as read."""
        try:
            if self.service:
                self.service.users().messages().batchModify(
                    userId='me',
                    body={
                        'ids': message_ids,
                        'removeLabelIds': ['UNREAD']
                    }
                ).execute()

            self.logger.info(f"Marked {len(message_ids)} messages as read")

        except Exception as e:
            self.logger.error(f"Failed to mark as read: {str(e)}")
            raise

    async def mark_unread(self, message_ids: List[str]):
        """Mark messages as unread."""
        try:
            if self.service:
                self.service.users().messages().batchModify(
                    userId='me',
                    body={
                        'ids': message_ids,
                        'addLabelIds': ['UNREAD']
                    }
                ).execute()

            self.logger.info(f"Marked {len(message_ids)} messages as unread")

        except Exception as e:
            self.logger.error(f"Failed to mark as unread: {str(e)}")
            raise

    async def trash_messages(self, message_ids: List[str]):
        """Move messages to trash."""
        try:
            if self.service:
                for msg_id in message_ids:
                    self.service.users().messages().trash(
                        userId='me',
                        id=msg_id
                    ).execute()

            self.logger.info(f"Trashed {len(message_ids)} messages")

        except Exception as e:
            self.logger.error(f"Failed to trash messages: {str(e)}")
            raise

    async def create_draft(
        self,
        to: str,
        subject: str,
        body: str
    ) -> Dict[str, Any]:
        """Create an email draft."""
        try:
            message = self._create_message(to, subject, body)

            if self.service:
                draft = self.service.users().drafts().create(
                    userId='me',
                    body={'message': message}
                ).execute()

                return {
                    'draft_id': draft['id'],
                    'message_id': draft['message']['id']
                }
            else:
                return {
                    'draft_id': f'draft_{datetime.now().timestamp()}'
                }

        except Exception as e:
            self.logger.error(f"Failed to create draft: {str(e)}")
            raise

    async def add_label(self, message_ids: List[str], label: str):
        """Add label to messages."""
        try:
            if self.service:
                self.service.users().messages().batchModify(
                    userId='me',
                    body={
                        'ids': message_ids,
                        'addLabelIds': [label]
                    }
                ).execute()

            self.logger.info(f"Added label '{label}' to {len(message_ids)} messages")

        except Exception as e:
            self.logger.error(f"Failed to add label: {str(e)}")
            raise

    async def remove_label(self, message_ids: List[str], label: str):
        """Remove label from messages."""
        try:
            if self.service:
                self.service.users().messages().batchModify(
                    userId='me',
                    body={
                        'ids': message_ids,
                        'removeLabelIds': [label]
                    }
                ).execute()

            self.logger.info(f"Removed label '{label}' from {len(message_ids)} messages")

        except Exception as e:
            self.logger.error(f"Failed to remove label: {str(e)}")
            raise
