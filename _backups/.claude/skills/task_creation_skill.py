"""Task Creation Skill - Task management across multiple platforms."""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta


class TaskCreationSkill:
    """Skill for creating and managing tasks across various task management platforms."""

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.logger = logging.getLogger("TaskCreationSkill")
        self.platforms = config.get("platforms", ["todoist", "asana", "trello"])
        self.tasks = []

    def create_task(
        self,
        platform: str,
        title: str,
        description: str = None,
        due_date: str = None,
        priority: str = "medium",
        labels: List[str] = None,
        assignee: str = None,
        project: str = None
    ) -> Dict[str, Any]:
        """
        Create a task on a specific platform.

        Args:
            platform: Platform name (todoist, asana, trello, jira)
            title: Task title
            description: Task description
            due_date: Due date (ISO format)
            priority: Priority level (low, medium, high, urgent)
            labels: List of labels/tags
            assignee: Person assigned to the task
            project: Project or board name

        Returns:
            Created task details
        """
        try:
            if platform not in self.platforms:
                return {"status": "error", "error": f"Platform {platform} not configured"}

            self.logger.info(f"Creating task on {platform}: {title}")

            task_id = f"{platform}_{len(self.tasks) + 1}"

            task = {
                "task_id": task_id,
                "platform": platform,
                "title": title,
                "description": description or "",
                "due_date": due_date,
                "priority": priority,
                "labels": labels or [],
                "assignee": assignee,
                "project": project,
                "status": "open",
                "created_at": datetime.now().isoformat(),
                "completed_at": None
            }

            self.tasks.append(task)

            # Placeholder for actual API call
            # Would use platform-specific API

            return {
                "status": "success",
                "task_id": task_id,
                "platform": platform,
                "title": title,
                "url": self._generate_task_url(platform, task_id)
            }

        except Exception as e:
            self.logger.error(f"Failed to create task: {str(e)}")
            return {"status": "error", "error": str(e)}

    def create_subtasks(
        self,
        platform: str,
        parent_task_id: str,
        subtasks: List[str]
    ) -> Dict[str, Any]:
        """
        Create subtasks under a parent task.

        Args:
            platform: Platform name
            parent_task_id: Parent task ID
            subtasks: List of subtask titles

        Returns:
            Created subtasks details
        """
        try:
            self.logger.info(f"Creating {len(subtasks)} subtasks for {parent_task_id}")

            created_subtasks = []

            for subtask_title in subtasks:
                result = self.create_task(
                    platform=platform,
                    title=subtask_title,
                    project=f"subtask_of_{parent_task_id}"
                )

                if result.get("status") == "success":
                    created_subtasks.append(result["task_id"])

            return {
                "status": "success",
                "parent_task_id": parent_task_id,
                "subtask_count": len(created_subtasks),
                "subtask_ids": created_subtasks
            }

        except Exception as e:
            self.logger.error(f"Failed to create subtasks: {str(e)}")
            return {"status": "error", "error": str(e)}

    def update_task(
        self,
        task_id: str,
        title: str = None,
        description: str = None,
        due_date: str = None,
        priority: str = None,
        status: str = None
    ) -> Dict[str, Any]:
        """
        Update an existing task.

        Args:
            task_id: Task identifier
            title: New title
            description: New description
            due_date: New due date
            priority: New priority
            status: New status

        Returns:
            Update result
        """
        try:
            task = self._find_task(task_id)

            if not task:
                return {"status": "error", "error": "Task not found"}

            if title:
                task["title"] = title
            if description:
                task["description"] = description
            if due_date:
                task["due_date"] = due_date
            if priority:
                task["priority"] = priority
            if status:
                task["status"] = status
                if status == "completed":
                    task["completed_at"] = datetime.now().isoformat()

            self.logger.info(f"Updated task: {task_id}")

            return {
                "status": "success",
                "task_id": task_id,
                "updated_fields": [k for k, v in locals().items() if v and k != "self" and k != "task_id"]
            }

        except Exception as e:
            self.logger.error(f"Failed to update task: {str(e)}")
            return {"status": "error", "error": str(e)}

    def complete_task(self, task_id: str) -> Dict[str, Any]:
        """Mark a task as completed."""
        return self.update_task(task_id, status="completed")

    def delete_task(self, task_id: str) -> Dict[str, Any]:
        """Delete a task."""
        try:
            task = self._find_task(task_id)

            if not task:
                return {"status": "error", "error": "Task not found"}

            self.tasks = [t for t in self.tasks if t["task_id"] != task_id]

            self.logger.info(f"Deleted task: {task_id}")

            return {
                "status": "success",
                "deleted": task_id
            }

        except Exception as e:
            self.logger.error(f"Failed to delete task: {str(e)}")
            return {"status": "error", "error": str(e)}

    def get_tasks(
        self,
        platform: str = None,
        status: str = None,
        priority: str = None,
        assignee: str = None
    ) -> List[Dict[str, Any]]:
        """
        Get tasks with optional filters.

        Args:
            platform: Filter by platform
            status: Filter by status
            priority: Filter by priority
            assignee: Filter by assignee

        Returns:
            List of matching tasks
        """
        filtered_tasks = self.tasks.copy()

        if platform:
            filtered_tasks = [t for t in filtered_tasks if t["platform"] == platform]
        if status:
            filtered_tasks = [t for t in filtered_tasks if t["status"] == status]
        if priority:
            filtered_tasks = [t for t in filtered_tasks if t["priority"] == priority]
        if assignee:
            filtered_tasks = [t for t in filtered_tasks if t["assignee"] == assignee]

        return filtered_tasks

    def get_overdue_tasks(self) -> List[Dict[str, Any]]:
        """Get all overdue tasks."""
        now = datetime.now()
        overdue = []

        for task in self.tasks:
            if task["status"] != "completed" and task["due_date"]:
                try:
                    due_date = datetime.fromisoformat(task["due_date"])
                    if due_date < now:
                        overdue.append(task)
                except:
                    pass

        return overdue

    def create_recurring_task(
        self,
        platform: str,
        title: str,
        recurrence: str,
        description: str = None,
        priority: str = "medium"
    ) -> Dict[str, Any]:
        """
        Create a recurring task.

        Args:
            platform: Platform name
            title: Task title
            recurrence: Recurrence pattern (daily, weekly, monthly)
            description: Task description
            priority: Priority level

        Returns:
            Created recurring task details
        """
        try:
            self.logger.info(f"Creating recurring task: {title} ({recurrence})")

            task_id = f"{platform}_recurring_{len(self.tasks) + 1}"

            task = {
                "task_id": task_id,
                "platform": platform,
                "title": title,
                "description": description or "",
                "priority": priority,
                "recurrence": recurrence,
                "status": "recurring",
                "created_at": datetime.now().isoformat()
            }

            self.tasks.append(task)

            return {
                "status": "success",
                "task_id": task_id,
                "recurrence": recurrence
            }

        except Exception as e:
            self.logger.error(f"Failed to create recurring task: {str(e)}")
            return {"status": "error", "error": str(e)}

    def bulk_create_tasks(
        self,
        platform: str,
        tasks: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Create multiple tasks at once.

        Args:
            platform: Platform name
            tasks: List of task dictionaries

        Returns:
            Bulk creation result
        """
        created = []
        failed = []

        for task_data in tasks:
            result = self.create_task(
                platform=platform,
                title=task_data.get("title", ""),
                description=task_data.get("description"),
                due_date=task_data.get("due_date"),
                priority=task_data.get("priority", "medium"),
                labels=task_data.get("labels"),
                assignee=task_data.get("assignee"),
                project=task_data.get("project")
            )

            if result.get("status") == "success":
                created.append(result["task_id"])
            else:
                failed.append(task_data.get("title"))

        return {
            "status": "success" if created else "error",
            "created": len(created),
            "failed": len(failed),
            "task_ids": created
        }

    def get_task_statistics(self, platform: str = None) -> Dict[str, Any]:
        """Get statistics about tasks."""
        tasks = self.get_tasks(platform=platform)

        total = len(tasks)
        completed = len([t for t in tasks if t["status"] == "completed"])
        open_tasks = len([t for t in tasks if t["status"] == "open"])
        overdue = len(self.get_overdue_tasks())

        by_priority = {
            "low": len([t for t in tasks if t["priority"] == "low"]),
            "medium": len([t for t in tasks if t["priority"] == "medium"]),
            "high": len([t for t in tasks if t["priority"] == "high"]),
            "urgent": len([t for t in tasks if t["priority"] == "urgent"])
        }

        return {
            "total": total,
            "completed": completed,
            "open": open_tasks,
            "overdue": overdue,
            "completion_rate": (completed / total * 100) if total > 0 else 0,
            "by_priority": by_priority
        }

    def _find_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Find a task by ID."""
        for task in self.tasks:
            if task["task_id"] == task_id:
                return task
        return None

    def _generate_task_url(self, platform: str, task_id: str) -> str:
        """Generate URL for a task."""
        base_urls = {
            "todoist": "https://todoist.com/app/task/",
            "asana": "https://app.asana.com/0/task/",
            "trello": "https://trello.com/c/",
            "jira": "https://jira.atlassian.com/browse/"
        }

        base = base_urls.get(platform, "https://example.com/task/")
        return f"{base}{task_id}"


def example_usage():
    """Example usage of task creation skill."""
    task_manager = TaskCreationSkill()

    # Create a single task
    task = task_manager.create_task(
        platform="todoist",
        title="Review project proposal",
        description="Review and provide feedback on Q2 project proposal",
        due_date=(datetime.now() + timedelta(days=3)).isoformat(),
        priority="high",
        labels=["review", "urgent"]
    )
    print(f"Created task: {task}\n")

    # Create subtasks
    subtasks = task_manager.create_subtasks(
        platform="todoist",
        parent_task_id=task["task_id"],
        subtasks=[
            "Read proposal document",
            "Check budget allocation",
            "Write feedback summary"
        ]
    )
    print(f"Created subtasks: {subtasks}\n")

    # Get all high priority tasks
    high_priority = task_manager.get_tasks(priority="high")
    print(f"High priority tasks: {len(high_priority)}\n")

    # Get statistics
    stats = task_manager.get_task_statistics()
    print(f"Task statistics: {stats}")


if __name__ == "__main__":
    example_usage()
