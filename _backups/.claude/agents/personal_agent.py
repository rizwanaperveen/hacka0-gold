"""Personal Agent - Handles personal tasks and communications."""

from typing import Any, Dict
from .base_agent import BaseAgent


class PersonalAgent(BaseAgent):
    """Agent for managing personal tasks, schedules, and communications."""

    def __init__(self, config=None):
        super().__init__("Personal Agent", config)
        self.calendar = []
        self.reminders = []

    def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process a personal task."""
        task_type = task.get("type", "general")

        if task_type == "schedule":
            return self._handle_schedule(task)
        elif task_type == "reminder":
            return self._handle_reminder(task)
        elif task_type == "communication":
            return self._handle_communication(task)
        else:
            return {"status": "completed", "message": f"Processed general task: {task.get('description')}"}

    def _handle_schedule(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle scheduling tasks."""
        event = task.get("event", {})
        self.calendar.append(event)
        return {"status": "completed", "message": f"Scheduled: {event.get('title', 'Event')}"}

    def _handle_reminder(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle reminder tasks."""
        reminder = task.get("reminder", {})
        self.reminders.append(reminder)
        return {"status": "completed", "message": f"Reminder set: {reminder.get('text', 'Reminder')}"}

    def _handle_communication(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle communication tasks."""
        message = task.get("message", "")
        recipient = task.get("recipient", "Unknown")
        return {"status": "completed", "message": f"Communication sent to {recipient}"}
