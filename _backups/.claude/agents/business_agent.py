"""Business Agent - Handles business operations and decisions."""

from typing import Any, Dict
from .base_agent import BaseAgent


class BusinessAgent(BaseAgent):
    """Agent for managing business tasks, operations, and analytics."""

    def __init__(self, config=None):
        super().__init__("Business Agent", config)
        self.projects = []
        self.analytics = {}

    def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process a business task."""
        task_type = task.get("type", "general")

        if task_type == "project":
            return self._handle_project(task)
        elif task_type == "analytics":
            return self._handle_analytics(task)
        elif task_type == "decision":
            return self._handle_decision(task)
        elif task_type == "report":
            return self._handle_report(task)
        else:
            return {"status": "completed", "message": f"Processed business task: {task.get('description')}"}

    def _handle_project(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle project management tasks."""
        project = task.get("project", {})
        self.projects.append(project)
        return {"status": "completed", "message": f"Project tracked: {project.get('name', 'Project')}"}

    def _handle_analytics(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle analytics tasks."""
        metric = task.get("metric", "")
        value = task.get("value", 0)
        self.analytics[metric] = value
        return {"status": "completed", "message": f"Analytics updated: {metric} = {value}"}

    def _handle_decision(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle business decision tasks."""
        decision = task.get("decision", "")
        options = task.get("options", [])
        return {"status": "completed", "message": f"Decision analyzed: {decision}", "options": options}

    def _handle_report(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle report generation tasks."""
        report_type = task.get("report_type", "general")
        return {"status": "completed", "message": f"Report generated: {report_type}"}
