"""
Integrations Layer - External API integrations

This package provides clean interfaces to all external services
used by the AI employee system.
"""

from integrations.base_integration import BaseIntegration
from integrations.gmail.gmail_client import GmailClient
from integrations.calendar.google_calendar_client import GoogleCalendarClient

__all__ = [
    "BaseIntegration",
    "GmailClient",
    "GoogleCalendarClient",
]
