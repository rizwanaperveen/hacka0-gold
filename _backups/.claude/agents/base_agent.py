"""Base Agent - Foundation class for all agents."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
import logging


class BaseAgent(ABC):
    """Abstract base class for all agents in the system."""

    def __init__(self, name: str, config: Optional[Dict[str, Any]] = None):
        self.name = name
        self.config = config or {}
        self.logger = logging.getLogger(f"Agent.{name}")
        self.status = "idle"
        self.task_queue: List[Dict[str, Any]] = []
        self.results: List[Dict[str, Any]] = []

    @abstractmethod
    def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process a single task. Must be implemented by subclasses."""
        pass

    def add_task(self, task: Dict[str, Any]) -> None:
        """Add a task to the agent's queue."""
        self.task_queue.append(task)
        self.logger.info(f"Task added: {task.get('description', 'No description')}")

    def get_status(self) -> str:
        """Get current agent status."""
        return self.status

    def set_status(self, status: str) -> None:
        """Set agent status."""
        self.status = status
        self.logger.info(f"Status changed to: {status}")

    def run(self) -> None:
        """Main execution loop for processing tasks."""
        self.set_status("running")

        while self.task_queue:
            task = self.task_queue.pop(0)
            self.logger.info(f"Processing task: {task.get('description', 'Unknown')}")

            try:
                result = self.process_task(task)
                self.results.append(result)
                self.logger.info(f"Task completed successfully")
            except Exception as e:
                self.logger.error(f"Task failed: {str(e)}")
                self.results.append({"status": "error", "error": str(e), "task": task})

        self.set_status("idle")

    def get_results(self) -> List[Dict[str, Any]]:
        """Get all task results."""
        return self.results

    def clear_results(self) -> None:
        """Clear all stored results."""
        self.results = []
