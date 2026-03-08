"""Task scheduler for automated agent tasks."""

import time
import threading
from typing import Dict, Any, List, Callable
from datetime import datetime, timedelta
import logging


class TaskScheduler:
    """Schedule and run tasks automatically at specified intervals."""

    def __init__(self, runner):
        self.runner = runner
        self.scheduled_tasks: List[Dict[str, Any]] = []
        self.running = False
        self.thread = None
        self.logger = logging.getLogger("TaskScheduler")

    def schedule_task(
        self,
        task: Dict[str, Any],
        interval: int = None,
        cron: str = None,
        run_at: str = None,
        repeat: bool = True
    ) -> str:
        """
        Schedule a task to run automatically.

        Args:
            task: The task to run
            interval: Run every N seconds
            cron: Cron expression (not implemented yet)
            run_at: ISO timestamp to run at
            repeat: Whether to repeat the task

        Returns:
            Schedule ID
        """
        schedule_id = f"schedule_{len(self.scheduled_tasks) + 1}"

        scheduled_task = {
            "id": schedule_id,
            "task": task,
            "interval": interval,
            "cron": cron,
            "run_at": run_at,
            "repeat": repeat,
            "last_run": None,
            "next_run": self._calculate_next_run(interval, run_at),
            "enabled": True
        }

        self.scheduled_tasks.append(scheduled_task)
        self.logger.info(f"Task scheduled: {schedule_id}")

        return schedule_id

    def _calculate_next_run(self, interval: int = None, run_at: str = None) -> datetime:
        """Calculate the next run time."""
        if run_at:
            return datetime.fromisoformat(run_at)
        elif interval:
            return datetime.now() + timedelta(seconds=interval)
        else:
            return datetime.now()

    def start(self):
        """Start the scheduler."""
        if self.running:
            self.logger.warning("Scheduler already running")
            return

        self.running = True
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()
        self.logger.info("Scheduler started")

    def stop(self):
        """Stop the scheduler."""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        self.logger.info("Scheduler stopped")

    def _run_loop(self):
        """Main scheduler loop."""
        while self.running:
            try:
                now = datetime.now()

                for scheduled_task in self.scheduled_tasks:
                    if not scheduled_task["enabled"]:
                        continue

                    next_run = scheduled_task["next_run"]

                    if now >= next_run:
                        self._execute_scheduled_task(scheduled_task)

                time.sleep(1)  # Check every second

            except Exception as e:
                self.logger.error(f"Scheduler error: {str(e)}")

    def _execute_scheduled_task(self, scheduled_task: Dict[str, Any]):
        """Execute a scheduled task."""
        try:
            task = scheduled_task["task"]
            self.logger.info(f"Running scheduled task: {scheduled_task['id']}")

            result = self.runner.run_task(task)

            scheduled_task["last_run"] = datetime.now()

            # Calculate next run
            if scheduled_task["repeat"] and scheduled_task["interval"]:
                scheduled_task["next_run"] = datetime.now() + timedelta(
                    seconds=scheduled_task["interval"]
                )
            else:
                scheduled_task["enabled"] = False

            self.logger.info(f"Scheduled task completed: {result.get('message')}")

        except Exception as e:
            self.logger.error(f"Error executing scheduled task: {str(e)}")

    def get_scheduled_tasks(self) -> List[Dict[str, Any]]:
        """Get all scheduled tasks."""
        return [
            {
                "id": st["id"],
                "task": st["task"],
                "interval": st["interval"],
                "last_run": st["last_run"].isoformat() if st["last_run"] else None,
                "next_run": st["next_run"].isoformat() if st["next_run"] else None,
                "enabled": st["enabled"]
            }
            for st in self.scheduled_tasks
        ]

    def enable_task(self, schedule_id: str):
        """Enable a scheduled task."""
        for task in self.scheduled_tasks:
            if task["id"] == schedule_id:
                task["enabled"] = True
                self.logger.info(f"Task enabled: {schedule_id}")
                return True
        return False

    def disable_task(self, schedule_id: str):
        """Disable a scheduled task."""
        for task in self.scheduled_tasks:
            if task["id"] == schedule_id:
                task["enabled"] = False
                self.logger.info(f"Task disabled: {schedule_id}")
                return True
        return False

    def remove_task(self, schedule_id: str):
        """Remove a scheduled task."""
        self.scheduled_tasks = [
            t for t in self.scheduled_tasks if t["id"] != schedule_id
        ]
        self.logger.info(f"Task removed: {schedule_id}")


def example_usage():
    """Example usage of the task scheduler."""
    from agent_runner import AgentRunner

    runner = AgentRunner()
    scheduler = TaskScheduler(runner)

    # Schedule a task to run every 60 seconds
    scheduler.schedule_task(
        task={
            "agent_type": "business",
            "type": "analytics",
            "metric": "health_check",
            "value": 1,
            "description": "Periodic health check"
        },
        interval=60,
        repeat=True
    )

    # Schedule a one-time task
    scheduler.schedule_task(
        task={
            "agent_type": "personal",
            "type": "reminder",
            "reminder": {"text": "Daily standup"},
            "description": "Daily reminder"
        },
        run_at=(datetime.now() + timedelta(hours=1)).isoformat(),
        repeat=False
    )

    # Start the scheduler
    scheduler.start()

    print("Scheduler running. Press Ctrl+C to stop.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        scheduler.stop()
        print("\nScheduler stopped")


if __name__ == "__main__":
    example_usage()
