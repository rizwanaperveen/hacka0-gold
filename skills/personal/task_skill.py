"""
Task Skill - Atomic task operations

Provides core task management functionality:
- Create tasks
- Read tasks
- Move tasks between folders
- Mark tasks complete
- Task prioritization
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from pathlib import Path
import shutil

from skills.base_skill import BaseSkill


class TaskSkill(BaseSkill):
    """
    Atomic skill for task operations.

    This skill provides low-level task management functionality
    for the AI employee vault system.
    """

    def __init__(self, vault_path: str = "AI_Employee_Vault"):
        super().__init__("task_management")
        self.vault_path = Path(vault_path)

        # Task folders
        self.folders = {
            "inbox": self.vault_path / "Inbox",
            "needs_action": self.vault_path / "Needs_Action",
            "pending_approval": self.vault_path / "Pending_Approval",
            "approved": self.vault_path / "Approved",
            "plans": self.vault_path / "Plans",
            "done": self.vault_path / "Done",
            "rejected": self.vault_path / "Rejected"
        }

        # Ensure folders exist
        for folder in self.folders.values():
            folder.mkdir(parents=True, exist_ok=True)

    async def execute(self, action: str, **kwargs) -> Dict[str, Any]:
        """Execute a task operation."""
        if action == "create":
            return await self.create_task(**kwargs)
        elif action == "read":
            return await self.read_task(**kwargs)
        elif action == "move":
            return await self.move_task(**kwargs)
        elif action == "complete":
            return await self.mark_complete(**kwargs)
        elif action == "list":
            return await self.list_tasks(**kwargs)
        else:
            return {"status": "error", "error": f"Unknown action: {action}"}

    async def create_task(
        self,
        title: str,
        description: str,
        folder: str = "inbox",
        priority: str = "medium",
        metadata: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Create a new task."""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            task_id = f"task_{timestamp}"
            filename = f"{task_id}.md"

            folder_path = self.folders.get(folder, self.folders["inbox"])

            content = f"""# {title}

**Created**: {datetime.now().isoformat()}
**Priority**: {priority}
**Status**: New

---

## Description

{description}

---

## Metadata

"""
            if metadata:
                for key, value in metadata.items():
                    content += f"- {key}: {value}\n"

            task_path = folder_path / filename
            with open(task_path, 'w') as f:
                f.write(content)

            self.logger.info(f"Created task: {filename}")
            await self._track_execution(True)

            return {
                "status": "success",
                "task_id": task_id,
                "filename": filename,
                "folder": folder,
                "path": str(task_path)
            }

        except Exception as e:
            self.logger.error(f"Failed to create task: {str(e)}")
            await self._track_execution(False)
            return {"status": "error", "error": str(e)}

    async def read_task(self, filename: str) -> Dict[str, Any]:
        """Read a task file."""
        try:
            # Search for task in all folders
            task_path = None
            for folder in self.folders.values():
                potential_path = folder / filename
                if potential_path.exists():
                    task_path = potential_path
                    break

            if not task_path:
                task_path = Path(filename)
                if not task_path.exists():
                    return {"status": "error", "error": "Task not found"}

            with open(task_path, 'r') as f:
                content = f.read()

            return {
                "status": "success",
                "content": content,
                "path": str(task_path)
            }

        except Exception as e:
            self.logger.error(f"Failed to read task: {str(e)}")
            return {"status": "error", "error": str(e)}

    async def move_task(
        self,
        filename: str,
        destination: str
    ) -> Dict[str, Any]:
        """Move a task to a different folder."""
        try:
            # Find current location
            source_path = None
            for folder in self.folders.values():
                potential_path = folder / filename
                if potential_path.exists():
                    source_path = potential_path
                    break

            if not source_path:
                return {"status": "error", "error": "Task not found"}

            # Get destination folder
            dest_folder = self.folders.get(destination)
            if not dest_folder:
                return {"status": "error", "error": f"Invalid destination: {destination}"}

            # Move file
            dest_path = dest_folder / filename
            shutil.move(str(source_path), str(dest_path))

            self.logger.info(f"Moved task {filename} to {destination}")
            await self._track_execution(True)

            return {
                "status": "success",
                "filename": filename,
                "destination": destination,
                "new_path": str(dest_path)
            }

        except Exception as e:
            self.logger.error(f"Failed to move task: {str(e)}")
            await self._track_execution(False)
            return {"status": "error", "error": str(e)}

    async def mark_complete(self, filename: str) -> Dict[str, Any]:
        """Mark a task as complete."""
        result = await self.move_task(filename, "done")
        return result

    async def list_tasks(
        self,
        folder: str = "needs_action",
        limit: int = 50
    ) -> Dict[str, Any]:
        """List tasks in a folder."""
        try:
            folder_path = self.folders.get(folder, self.folders["needs_action"])

            if not folder_path.exists():
                return {"status": "error", "error": f"Folder not found: {folder}"}

            task_files = list(folder_path.glob("*.md"))[:limit]

            tasks = []
            for task_file in task_files:
                tasks.append({
                    "filename": task_file.name,
                    "path": str(task_file),
                    "created": datetime.fromtimestamp(
                        task_file.stat().st_ctime
                    ).isoformat()
                })

            return {
                "status": "success",
                "folder": folder,
                "count": len(tasks),
                "tasks": tasks
            }

        except Exception as e:
            self.logger.error(f"Failed to list tasks: {str(e)}")
            return {"status": "error", "error": str(e)}

    async def get_pending_tasks(self) -> List[Dict[str, Any]]:
        """Get all pending tasks from Needs_Action folder."""
        result = await self.list_tasks("needs_action")
        return result.get("tasks", [])

    async def get_task_statistics(self) -> Dict[str, Any]:
        """Get task statistics across all folders."""
        stats = {}

        for folder_name, folder_path in self.folders.items():
            if folder_path.exists():
                count = len(list(folder_path.glob("*.md")))
                stats[folder_name] = count

        return {
            "status": "success",
            "statistics": stats,
            "total": sum(stats.values())
        }
