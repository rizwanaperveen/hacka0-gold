"""Webhook and notification system for the multi-agent system."""

import requests
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime


class WebhookManager:
    """Manage webhooks for agent events."""

    def __init__(self):
        self.webhooks: Dict[str, List[str]] = {
            "task_started": [],
            "task_completed": [],
            "task_failed": [],
            "agent_status_changed": [],
            "system_alert": []
        }
        self.logger = logging.getLogger("WebhookManager")

    def register_webhook(self, event_type: str, url: str) -> bool:
        """Register a webhook URL for an event type."""
        if event_type not in self.webhooks:
            self.logger.error(f"Invalid event type: {event_type}")
            return False

        if url not in self.webhooks[event_type]:
            self.webhooks[event_type].append(url)
            self.logger.info(f"Webhook registered: {event_type} -> {url}")
            return True

        return False

    def unregister_webhook(self, event_type: str, url: str) -> bool:
        """Unregister a webhook URL."""
        if event_type in self.webhooks and url in self.webhooks[event_type]:
            self.webhooks[event_type].remove(url)
            self.logger.info(f"Webhook unregistered: {event_type} -> {url}")
            return True

        return False

    def trigger_webhook(self, event_type: str, data: Dict[str, Any]) -> None:
        """Trigger all webhooks for an event type."""
        if event_type not in self.webhooks:
            return

        payload = {
            "event": event_type,
            "timestamp": datetime.now().isoformat(),
            "data": data
        }

        for url in self.webhooks[event_type]:
            try:
                response = requests.post(
                    url,
                    json=payload,
                    timeout=5,
                    headers={"Content-Type": "application/json"}
                )
                response.raise_for_status()
                self.logger.info(f"Webhook triggered successfully: {url}")
            except Exception as e:
                self.logger.error(f"Webhook failed: {url} - {str(e)}")

    def get_webhooks(self) -> Dict[str, List[str]]:
        """Get all registered webhooks."""
        return self.webhooks.copy()


class NotificationManager:
    """Manage notifications for agent events."""

    def __init__(self):
        self.channels: Dict[str, Any] = {}
        self.logger = logging.getLogger("NotificationManager")

    def add_channel(self, name: str, channel_type: str, config: Dict[str, Any]) -> None:
        """Add a notification channel."""
        self.channels[name] = {
            "type": channel_type,
            "config": config,
            "enabled": True
        }
        self.logger.info(f"Notification channel added: {name} ({channel_type})")

    def remove_channel(self, name: str) -> bool:
        """Remove a notification channel."""
        if name in self.channels:
            del self.channels[name]
            self.logger.info(f"Notification channel removed: {name}")
            return True
        return False

    def send_notification(self, message: str, level: str = "info", channels: List[str] = None) -> None:
        """Send a notification to specified channels."""
        target_channels = channels if channels else list(self.channels.keys())

        for channel_name in target_channels:
            if channel_name not in self.channels:
                continue

            channel = self.channels[channel_name]

            if not channel["enabled"]:
                continue

            try:
                if channel["type"] == "slack":
                    self._send_slack(message, level, channel["config"])
                elif channel["type"] == "email":
                    self._send_email(message, level, channel["config"])
                elif channel["type"] == "console":
                    self._send_console(message, level)
                else:
                    self.logger.warning(f"Unknown channel type: {channel['type']}")

            except Exception as e:
                self.logger.error(f"Notification failed for {channel_name}: {str(e)}")

    def _send_slack(self, message: str, level: str, config: Dict[str, Any]) -> None:
        """Send notification to Slack."""
        webhook_url = config.get("webhook_url")

        if not webhook_url:
            raise ValueError("Slack webhook_url not configured")

        color_map = {
            "info": "#36a64f",
            "warning": "#ff9800",
            "error": "#f44336"
        }

        payload = {
            "attachments": [{
                "color": color_map.get(level, "#36a64f"),
                "text": message,
                "footer": "Multi-Agent System",
                "ts": int(datetime.now().timestamp())
            }]
        }

        response = requests.post(webhook_url, json=payload, timeout=5)
        response.raise_for_status()

    def _send_email(self, message: str, level: str, config: Dict[str, Any]) -> None:
        """Send notification via email."""
        # Placeholder for email implementation
        # Would use smtplib in a real implementation
        self.logger.info(f"Email notification: {message}")

    def _send_console(self, message: str, level: str) -> None:
        """Send notification to console."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] [{level.upper()}] {message}")


class EventBus:
    """Event bus for agent system events."""

    def __init__(self):
        self.subscribers: Dict[str, List[callable]] = {}
        self.logger = logging.getLogger("EventBus")

    def subscribe(self, event_type: str, callback: callable) -> None:
        """Subscribe to an event type."""
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []

        self.subscribers[event_type].append(callback)
        self.logger.info(f"Subscriber added for event: {event_type}")

    def unsubscribe(self, event_type: str, callback: callable) -> bool:
        """Unsubscribe from an event type."""
        if event_type in self.subscribers and callback in self.subscribers[event_type]:
            self.subscribers[event_type].remove(callback)
            self.logger.info(f"Subscriber removed for event: {event_type}")
            return True
        return False

    def publish(self, event_type: str, data: Dict[str, Any]) -> None:
        """Publish an event to all subscribers."""
        if event_type not in self.subscribers:
            return

        event = {
            "type": event_type,
            "timestamp": datetime.now().isoformat(),
            "data": data
        }

        for callback in self.subscribers[event_type]:
            try:
                callback(event)
            except Exception as e:
                self.logger.error(f"Event callback failed: {str(e)}")


def setup_notifications(runner, webhook_manager: WebhookManager, notification_manager: NotificationManager):
    """Setup notifications for agent events."""

    # Add console notification channel
    notification_manager.add_channel("console", "console", {})

    # Example: Add Slack channel (uncomment and configure)
    # notification_manager.add_channel("slack", "slack", {
    #     "webhook_url": "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
    # })

    # Notify on task completion
    def on_task_complete(result):
        if result.get("status") == "completed":
            notification_manager.send_notification(
                f"Task completed: {result.get('message')}",
                level="info"
            )
        else:
            notification_manager.send_notification(
                f"Task failed: {result.get('message')}",
                level="error"
            )

    return on_task_complete
