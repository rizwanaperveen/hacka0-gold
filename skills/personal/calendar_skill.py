"""
Calendar Skill - Atomic calendar operations

Provides core calendar functionality:
- Create events
- Read events
- Update events
- Delete events
- Check availability
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta

from skills.base_skill import BaseSkill


class CalendarSkill(BaseSkill):
    """
    Atomic skill for calendar operations.

    This skill provides low-level calendar management functionality
    for scheduling and event management.
    """

    def __init__(self, calendar_client=None):
        super().__init__("calendar_management")
        self.calendar_client = calendar_client

    async def execute(self, action: str, **kwargs) -> Dict[str, Any]:
        """Execute a calendar operation."""
        if action == "create_event":
            return await self.create_event(**kwargs)
        elif action == "get_events":
            return await self.get_events(**kwargs)
        elif action == "update_event":
            return await self.update_event(**kwargs)
        elif action == "delete_event":
            return await self.delete_event(**kwargs)
        elif action == "check_availability":
            return await self.check_availability(**kwargs)
        else:
            return {"status": "error", "error": f"Unknown action: {action}"}

    async def create_event(
        self,
        title: str,
        start_time: str,
        end_time: str,
        description: str = None,
        attendees: List[str] = None,
        location: str = None,
        reminders: bool = True
    ) -> Dict[str, Any]:
        """Create a calendar event."""
        try:
            self.logger.info(f"Creating event: {title}")

            if self.calendar_client:
                result = await self.calendar_client.create_event(
                    title=title,
                    start_time=start_time,
                    end_time=end_time,
                    description=description,
                    attendees=attendees,
                    location=location,
                    reminders=reminders
                )
            else:
                # Placeholder
                result = {
                    "event_id": f"event_{datetime.now().timestamp()}",
                    "status": "created"
                }

            await self._track_execution(True)

            return {
                "status": "success",
                "event_id": result.get("event_id"),
                "title": title,
                "start_time": start_time
            }

        except Exception as e:
            self.logger.error(f"Failed to create event: {str(e)}")
            await self._track_execution(False)
            return {"status": "error", "error": str(e)}

    async def get_events(
        self,
        start_date: str = None,
        end_date: str = None,
        max_results: int = 50
    ) -> Dict[str, Any]:
        """Get calendar events."""
        try:
            self.logger.info("Getting calendar events")

            if not start_date:
                start_date = datetime.now().isoformat()
            if not end_date:
                end_date = (datetime.now() + timedelta(days=7)).isoformat()

            if self.calendar_client:
                events = await self.calendar_client.list_events(
                    start_date=start_date,
                    end_date=end_date,
                    max_results=max_results
                )
            else:
                # Placeholder
                events = []

            return {
                "status": "success",
                "events": events,
                "count": len(events)
            }

        except Exception as e:
            self.logger.error(f"Failed to get events: {str(e)}")
            return {"status": "error", "error": str(e)}

    async def update_event(
        self,
        event_id: str,
        **updates
    ) -> Dict[str, Any]:
        """Update a calendar event."""
        try:
            self.logger.info(f"Updating event: {event_id}")

            if self.calendar_client:
                result = await self.calendar_client.update_event(
                    event_id=event_id,
                    **updates
                )
            else:
                result = {"status": "updated"}

            await self._track_execution(True)

            return {
                "status": "success",
                "event_id": event_id,
                "updates": updates
            }

        except Exception as e:
            self.logger.error(f"Failed to update event: {str(e)}")
            await self._track_execution(False)
            return {"status": "error", "error": str(e)}

    async def delete_event(self, event_id: str) -> Dict[str, Any]:
        """Delete a calendar event."""
        try:
            self.logger.info(f"Deleting event: {event_id}")

            if self.calendar_client:
                await self.calendar_client.delete_event(event_id)

            await self._track_execution(True)

            return {
                "status": "success",
                "event_id": event_id,
                "deleted": True
            }

        except Exception as e:
            self.logger.error(f"Failed to delete event: {str(e)}")
            await self._track_execution(False)
            return {"status": "error", "error": str(e)}

    async def check_availability(
        self,
        start_time: str,
        end_time: str,
        buffer_minutes: int = 15
    ) -> Dict[str, Any]:
        """Check availability for a time slot."""
        try:
            self.logger.info(f"Checking availability: {start_time} - {end_time}")

            # Get events in the time range
            events_result = await self.get_events(
                start_date=start_time,
                end_date=end_time
            )

            events = events_result.get("events", [])

            # Check for conflicts
            has_conflict = len(events) > 0

            await self._track_execution(True)

            return {
                "status": "success",
                "available": not has_conflict,
                "conflicts": events if has_conflict else [],
                "buffer_minutes": buffer_minutes
            }

        except Exception as e:
            self.logger.error(f"Failed to check availability: {str(e)}")
            return {"status": "error", "error": str(e)}
