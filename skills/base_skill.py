"""
Base Skill - Abstract base class for all atomic skills

Provides common functionality and interface for:
- Skill execution
- Error handling
- Validation
- Result formatting
"""

import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from datetime import datetime


class BaseSkill(ABC):
    """
    Abstract base class for all atomic skills.

    Skills are the lowest level of executable capabilities in the system.
    They are composable, testable, and domain-agnostic.
    """

    def __init__(self, name: str, config: Dict[str, Any] = None):
        self.name = name
        self.config = config or {}

        self.logger = logging.getLogger(f"{self.__class__.__name__}")

        # Skill state
        self.state = {
            "enabled": True,
            "executions": 0,
            "successes": 0,
            "failures": 0,
            "last_execution": None
        }

        self.logger.info(f"Skill '{name}' initialized")

    @abstractmethod
    async def execute(self, **kwargs) -> Dict[str, Any]:
        """
        Execute the skill with provided parameters.

        Args:
            **kwargs: Skill-specific parameters

        Returns:
            Result dictionary with status and output
        """
        pass

    def validate(self, **kwargs) -> Dict[str, Any]:
        """
        Validate input parameters before execution.

        Args:
            **kwargs: Parameters to validate

        Returns:
            Validation result with 'valid' boolean and 'errors' list
        """
        return {
            "valid": True,
            "errors": []
        }

    def get_status(self) -> Dict[str, Any]:
        """Get current skill status."""
        success_rate = 0.0
        if self.state["executions"] > 0:
            success_rate = (self.state["successes"] / self.state["executions"]) * 100

        return {
            "name": self.name,
            "enabled": self.state["enabled"],
            "executions": self.state["executions"],
            "success_rate": success_rate,
            "last_execution": self.state["last_execution"]
        }

    def enable(self):
        """Enable the skill."""
        self.state["enabled"] = True
        self.logger.info(f"Skill '{self.name}' enabled")

    def disable(self):
        """Disable the skill."""
        self.state["enabled"] = False
        self.logger.info(f"Skill '{self.name}' disabled")

    async def _track_execution(self, success: bool):
        """Track execution statistics."""
        self.state["executions"] += 1
        self.state["last_execution"] = datetime.now().isoformat()

        if success:
            self.state["successes"] += 1
        else:
            self.state["failures"] += 1
