"""
Email Skill - Atomic email operations

Provides core email functionality:
- Send emails
- Read emails
- Search emails
- Manage labels
- Handle attachments
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime


class EmailSkill:
    """
    Atomic skill for email operations.

    This skill provides low-level email functionality that can be
    composed into higher-level workflows by agents.
    """

    def __init__(self, gmail_client=None):
        self.logger = logging.getLogger("EmailSkill")
        self.gmail_client = gmail_client

        self.logger.info("Email skill initialized")

    async def send_email(
        self,
        to: str,
        subject: str,
        body: str,
        cc: List[str] = None,
        bcc: List[str] = None,
        attachments: List[str] = None
    ) -> Dict[str, Any]:
        """
        Send an email.

        Args:
            to: Recipient email address
            subject: Email subject
            body: Email body
            cc: CC recipients
            bcc: BCC recipients
            attachments: List of attachment file paths

        Returns:
            Result dictionary
        """
        try:
            self.logger.info(f"Sending email to {to}: {subject}")

            if self.gmail_client:
                result = await self.gmail_client.send_message(
                    to=to,
                    subject=subject,
                    body=body,
                    cc=cc,
                    bcc=bcc,
                    attachments=attachments
                )
            else:
                # Placeholder when no client available
                result = {
                    "message_id": f"msg_{datetime.now().timestamp()}",
                    "status": "sent"
                }

            return {
                "status": "success",
                "message_id": result.get("message_id"),
                "to": to,
                "subject": subject
            }

        except Exception as e:
            self.logger.error(f"Failed to send email: {str(e)}")
            return {
                "status": "error",
                "error": str(e)
            }

    async def read_emails(
        self,
        query: str = None,
        max_results: int = 10,
        unread_only: bool = False,
        labels: List[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Read emails from inbox.

        Args:
            query: Search query
            max_results: Maximum number of emails to return
            unread_only: Only return unread emails
            labels: Filter by labels

        Returns:
            List of email dictionaries
        """
        try:
            self.logger.info(f"Reading emails (query: {query}, max: {max_results})")

            if self.gmail_client:
                emails = await self.gmail_client.list_messages(
                    query=query,
                    max_results=max_results,
                    unread_only=unread_only,
                    labels=labels
                )
            else:
                # Placeholder
                emails = []

            return emails

        except Exception as e:
            self.logger.error(f"Failed to read emails: {str(e)}")
            return []

    async def search_emails(
        self,
        from_email: str = None,
        to_email: str = None,
        subject: str = None,
        has_attachment: bool = None,
        after_date: str = None,
        before_date: str = None
    ) -> List[Dict[str, Any]]:
        """
        Search emails with specific criteria.

        Args:
            from_email: Filter by sender
            to_email: Filter by recipient
            subject: Filter by subject keywords
            has_attachment: Filter emails with attachments
            after_date: Filter emails after date
            before_date: Filter emails before date

        Returns:
            List of matching emails
        """
        # Build query string
        query_parts = []

        if from_email:
            query_parts.append(f"from:{from_email}")
        if to_email:
            query_parts.append(f"to:{to_email}")
        if subject:
            query_parts.append(f"subject:{subject}")
        if has_attachment:
            query_parts.append("has:attachment")
        if after_date:
            query_parts.append(f"after:{after_date}")
        if before_date:
            query_parts.append(f"before:{before_date}")

        query = " ".join(query_parts)

        return await self.read_emails(query=query)

    async def mark_as_read(self, message_ids: List[str]) -> Dict[str, Any]:
        """Mark emails as read."""
        try:
            self.logger.info(f"Marking {len(message_ids)} emails as read")

            if self.gmail_client:
                await self.gmail_client.mark_read(message_ids)

            return {
                "status": "success",
                "marked": len(message_ids)
            }

        except Exception as e:
            self.logger.error(f"Failed to mark as read: {str(e)}")
            return {
                "status": "error",
                "error": str(e)
            }

    async def mark_as_unread(self, message_ids: List[str]) -> Dict[str, Any]:
        """Mark emails as unread."""
        try:
            self.logger.info(f"Marking {len(message_ids)} emails as unread")

            if self.gmail_client:
                await self.gmail_client.mark_unread(message_ids)

            return {
                "status": "success",
                "marked": len(message_ids)
            }

        except Exception as e:
            self.logger.error(f"Failed to mark as unread: {str(e)}")
            return {
                "status": "error",
                "error": str(e)
            }

    async def delete_emails(self, message_ids: List[str]) -> Dict[str, Any]:
        """Delete emails."""
        try:
            self.logger.info(f"Deleting {len(message_ids)} emails")

            if self.gmail_client:
                await self.gmail_client.trash_messages(message_ids)

            return {
                "status": "success",
                "deleted": len(message_ids)
            }

        except Exception as e:
            self.logger.error(f"Failed to delete emails: {str(e)}")
            return {
                "status": "error",
                "error": str(e)
            }

    async def create_draft(
        self,
        to: str,
        subject: str,
        body: str
    ) -> Dict[str, Any]:
        """Create an email draft."""
        try:
            self.logger.info(f"Creating draft to {to}: {subject}")

            if self.gmail_client:
                result = await self.gmail_client.create_draft(
                    to=to,
                    subject=subject,
                    body=body
                )
            else:
                result = {
                    "draft_id": f"draft_{datetime.now().timestamp()}"
                }

            return {
                "status": "success",
                "draft_id": result.get("draft_id"),
                "to": to,
                "subject": subject
            }

        except Exception as e:
            self.logger.error(f"Failed to create draft: {str(e)}")
            return {
                "status": "error",
                "error": str(e)
            }

    async def apply_label(
        self,
        message_ids: List[str],
        label: str
    ) -> Dict[str, Any]:
        """Apply a label to emails."""
        try:
            self.logger.info(f"Applying label '{label}' to {len(message_ids)} emails")

            if self.gmail_client:
                await self.gmail_client.add_label(message_ids, label)

            return {
                "status": "success",
                "labeled": len(message_ids),
                "label": label
            }

        except Exception as e:
            self.logger.error(f"Failed to apply label: {str(e)}")
            return {
                "status": "error",
                "error": str(e)
            }

    async def remove_label(
        self,
        message_ids: List[str],
        label: str
    ) -> Dict[str, Any]:
        """Remove a label from emails."""
        try:
            self.logger.info(f"Removing label '{label}' from {len(message_ids)} emails")

            if self.gmail_client:
                await self.gmail_client.remove_label(message_ids, label)

            return {
                "status": "success",
                "unlabeled": len(message_ids),
                "label": label
            }

        except Exception as e:
            self.logger.error(f"Failed to remove label: {str(e)}")
            return {
                "status": "error",
                "error": str(e)
            }
