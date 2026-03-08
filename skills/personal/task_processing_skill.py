"""
Task Processing Skill - Process tasks from Needs_Action folder

Atomic skill for task processing operations.
"""

import logging
from typing import Dict, Any, List
from pathlib import Path
from datetime import datetime
import yaml


class TaskProcessingSkill:
    """
    Atomic skill for processing tasks.

    Handles:
    - Reading tasks from Needs_Action folder
    - Parsing task metadata
    - Categorizing tasks
    - Moving tasks between folders
    """

    def __init__(self, vault_path: str = "AI_Employee_Vault"):
        self.logger = logging.getLogger("TaskProcessingSkill")
        self.vault_path = Path(vault_path)

        # Folder paths
        self.needs_action = self.vault_path / "Needs_Action"
        self.plans = self.vault_path / "Plans"
        self.pending_approval = self.vault_path / "Pending_Approval"
        self.approved = self.vault_path / "Approved"
        self.done = self.vault_path / "Done"

        # Ensure folders exist
        for folder in [self.needs_action, self.plans, self.pending_approval, self.approved, self.done]:
            folder.mkdir(parents=True, exist_ok=True)

        self.logger.info("Task processing skill initialized")

    async def get_pending_tasks(self) -> List[Dict[str, Any]]:
        """Get all pending tasks from Needs_Action folder."""
        try:
            tasks = []

            for task_file in self.needs_action.glob("*.md"):
                task = await self.read_task(task_file)
                if task:
                    tasks.append(task)

            self.logger.info(f"Found {len(tasks)} pending tasks")
            return tasks

        except Exception as e:
            self.logger.error(f"Failed to get pending tasks: {str(e)}")
            return []

    async def read_task(self, task_file: Path) -> Dict[str, Any]:
        """Read and parse a task file."""
        try:
            with open(task_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Parse YAML frontmatter if present
            metadata = {}
            body = content

            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    try:
                        metadata = yaml.safe_load(parts[1])
                        body = parts[2].strip()
                    except:
                        pass

            return {
                "file": str(task_file),
                "filename": task_file.name,
                "metadata": metadata,
                "content": body,
                "created": datetime.fromtimestamp(task_file.stat().st_ctime).isoformat()
            }

        except Exception as e:
            self.logger.error(f"Failed to read task {task_file}: {str(e)}")
            return None

    async def categorize_task(self, task: Dict[str, Any]) -> str:
        """Categorize a task based on content and metadata."""
        content = task.get("content", "").lower()
        metadata = task.get("metadata", {})

        # Check metadata first
        if "category" in metadata:
            return metadata["category"]

        # Categorize based on keywords
        if any(word in content for word in ["email", "reply", "respond", "message"]):
            return "email"
        elif any(word in content for word in ["meeting", "schedule", "calendar"]):
            return "scheduling"
        elif any(word in content for word in ["post", "social", "linkedin", "twitter"]):
            return "social_media"
        elif any(word in content for word in ["project", "task", "todo"]):
            return "project_management"
        else:
            return "general"

    async def prioritize_task(self, task: Dict[str, Any]) -> int:
        """Determine task priority (1-5, 5 being highest)."""
        content = task.get("content", "").lower()
        metadata = task.get("metadata", {})

        # Check metadata first
        if "priority" in metadata:
            return int(metadata["priority"])

        # Determine priority based on keywords
        if any(word in content for word in ["urgent", "asap", "critical", "emergency"]):
            return 5
        elif any(word in content for word in ["important", "high priority"]):
            return 4
        elif any(word in content for word in ["soon", "today"]):
            return 3
        elif any(word in content for word in ["this week", "upcoming"]):
            return 2
        else:
            return 1

    async def move_task(
        self,
        task_file: str,
        destination: str
    ) -> Dict[str, Any]:
        """
        Move a task file to a different folder.

        Args:
            task_file: Path to task file
            destination: Destination folder name (Plans, Pending_Approval, Approved, Done)

        Returns:
            Result dictionary
        """
        try:
            source_path = Path(task_file)

            # Determine destination folder
            dest_folders = {
                "Plans": self.plans,
                "Pending_Approval": self.pending_approval,
                "Approved": self.approved,
                "Done": self.done
            }

            if destination not in dest_folders:
                return {
                    "status": "error",
                    "error": f"Invalid destination: {destination}"
                }

            dest_folder = dest_folders[destination]
            dest_path = dest_folder / source_path.name

            # Move file
            source_path.rename(dest_path)

            self.logger.info(f"Moved task {source_path.name} to {destination}")

            return {
                "status": "success",
                "source": str(source_path),
                "destination": str(dest_path)
            }

        except Exception as e:
            self.logger.error(f"Failed to move task: {str(e)}")
            return {
                "status": "error",
                "error": str(e)
            }

    async def create_plan(
        self,
        task: Dict[str, Any],
        plan_content: str
    ) -> Dict[str, Any]:
        """
        Create a plan file for a task.

        Args:
            task: Task dictionary
            plan_content: Plan content in markdown

        Returns:
            Result dictionary
        """
        try:
            # Generate plan filename
            task_name = Path(task["filename"]).stem
            plan_filename = f"plan_{task_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
            plan_path = self.plans / plan_filename

            # Create plan file
            with open(plan_path, 'w', encoding='utf-8') as f:
                f.write(f"---\n")
                f.write(f"task: {task['filename']}\n")
                f.write(f"created: {datetime.now().isoformat()}\n")
                f.write(f"status: draft\n")
                f.write(f"---\n\n")
                f.write(plan_content)

            self.logger.info(f"Created plan: {plan_filename}")

            return {
                "status": "success",
                "plan_file": str(plan_path),
                "plan_filename": plan_filename
            }

        except Exception as e:
            self.logger.error(f"Failed to create plan: {str(e)}")
            return {
                "status": "error",
                "error": str(e)
            }

    async def mark_complete(self, task_file: str) -> Dict[str, Any]:
        """Mark a task as complete by moving to Done folder."""
        return await self.move_task(task_file, "Done")

    async def get_task_statistics(self) -> Dict[str, Any]:
        """Get statistics about tasks."""
        try:
            stats = {
                "needs_action": len(list(self.needs_action.glob("*.md"))),
                "plans": len(list(self.plans.glob("*.md"))),
                "pending_approval": len(list(self.pending_approval.glob("*.md"))),
                "approved": len(list(self.approved.glob("*.md"))),
                "done": len(list(self.done.glob("*.md")))
            }

            stats["total"] = sum(stats.values())

            return stats

        except Exception as e:
            self.logger.error(f"Failed to get statistics: {str(e)}")
            return {}
