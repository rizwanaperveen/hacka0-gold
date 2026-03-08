"""
Base Agent - Abstract base class for all decision-making agents

Provides common functionality and interface for:
- Task execution
- Status reporting
- Lifecycle management
- Audit logging integration
"""

import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from datetime import datetime


class BaseAgent(ABC):
    """
    Abstract base class for all decision-making agents.

    All domain-specific agents should inherit from this base class
    to ensure consistent interface and behavior across the system.
    """

    def __init__(
        self,
        domain: str,
        audit_logger=None,
        error_handler=None,
        config: Dict[str, Any] = None
    ):
        self.domain = domain
        self.audit_logger = audit_logger
        self.error_handler = error_handler
        self.config = config or {}

        self.logger = logging.getLogger(f"{self.__class__.__name__}")

        # Agent state
        self.state = {
            "active": True,
            "tasks_executed": 0,
            "tasks_succeeded": 0,
            "tasks_failed": 0,
            "last_task": None,
            "initialized_at": datetime.now().isoformat()
        }

        self.logger.info(f"{self.__class__.__name__} initialized for {domain} domain")

    @abstractmethod
    async def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a task in this agent's domain.

        Args:
            task: Task dictionary with type, description, etc.

        Returns:
            Result dictionary with status and output
        """
        pass

    async def execute_action(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a specific action.

        Args:
            action: Action dictionary

        Returns:
            Action result
        """
        action_type = action.get("action")
        self.logger.info(f"Executing action: {action_type}")

        return {
            "status": "success",
            "action": action_type,
            "domain": self.domain
        }

    def get_status(self) -> Dict[str, Any]:
        """Get current agent status."""
        return {
            "domain": self.domain,
            "active": self.state["active"],
            "tasks_executed": self.state["tasks_executed"],
            "success_rate": self._calculate_success_rate(),
            "initialized_at": self.state["initialized_at"]
        }

    def _calculate_success_rate(self) -> float:
        """Calculate task success rate."""
        if self.state["tasks_executed"] == 0:
            return 100.0

        return (
            self.state["tasks_succeeded"] / self.state["tasks_executed"]
        ) * 100

    def get_performance(self) -> Dict[str, Any]:
        """Get performance metrics."""
        return {
            "domain": self.domain,
            "tasks_completed": self.state["tasks_succeeded"],
            "tasks_failed": self.state["tasks_failed"],
            "success_rate": self._calculate_success_rate()
        }

    async def get_summary(self, period: str) -> Dict[str, Any]:
        """
        Get summary for specified period.

        Args:
            period: Time period (daily, weekly, monthly)

        Returns:
            Summary dictionary
        """
        return {
            "period": period,
            "tasks_completed": self.state["tasks_succeeded"],
            "success_rate": self._calculate_success_rate(),
            "key_activities": []
        }

    async def shutdown(self):
        """Shutdown the agent gracefully."""
        self.logger.info(f"Shutting down {self.__class__.__name__}")
        self.state["active"] = False
