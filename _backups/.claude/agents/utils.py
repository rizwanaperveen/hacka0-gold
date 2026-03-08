"""Utility functions for the multi-agent system."""

import json
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime


def load_config(config_path: str) -> Dict[str, Any]:
    """Load configuration from a JSON file."""
    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    with open(path, 'r') as f:
        return json.load(f)


def save_config(config: Dict[str, Any], config_path: str) -> None:
    """Save configuration to a JSON file."""
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)


def load_tasks(tasks_path: str) -> List[Dict[str, Any]]:
    """Load tasks from a JSON file."""
    path = Path(tasks_path)
    if not path.exists():
        raise FileNotFoundError(f"Tasks file not found: {tasks_path}")

    with open(path, 'r') as f:
        return json.load(f)


def save_results(results: List[Dict[str, Any]], output_path: str) -> None:
    """Save results to a JSON file."""
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)


def format_task(agent_type: str, task_type: str, description: str, **kwargs) -> Dict[str, Any]:
    """Format a task dictionary with proper structure."""
    task = {
        "agent_type": agent_type,
        "type": task_type,
        "description": description,
        "timestamp": datetime.now().isoformat()
    }
    task.update(kwargs)
    return task


def validate_task(task: Dict[str, Any]) -> tuple[bool, Optional[str]]:
    """Validate a task dictionary."""
    required_fields = ["agent_type", "type", "description"]

    for field in required_fields:
        if field not in task:
            return False, f"Missing required field: {field}"

    valid_agents = ["personal", "business", "social", "ceo", "autonomous"]
    if task["agent_type"] not in valid_agents:
        return False, f"Invalid agent_type: {task['agent_type']}"

    return True, None


def setup_logging(log_level: str = "INFO", log_file: Optional[str] = None) -> None:
    """Setup logging configuration."""
    handlers = [logging.StreamHandler()]

    if log_file:
        handlers.append(logging.FileHandler(log_file))

    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=handlers
    )


def create_personal_task(task_type: str, **kwargs) -> Dict[str, Any]:
    """Create a personal agent task."""
    return format_task("personal", task_type, kwargs.get("description", ""), **kwargs)


def create_business_task(task_type: str, **kwargs) -> Dict[str, Any]:
    """Create a business agent task."""
    return format_task("business", task_type, kwargs.get("description", ""), **kwargs)


def create_social_task(task_type: str, **kwargs) -> Dict[str, Any]:
    """Create a social agent task."""
    return format_task("social", task_type, kwargs.get("description", ""), **kwargs)


def create_ceo_task(task_type: str, **kwargs) -> Dict[str, Any]:
    """Create a CEO agent task."""
    return format_task("ceo", task_type, kwargs.get("description", ""), **kwargs)


def create_autonomous_task(task_type: str, **kwargs) -> Dict[str, Any]:
    """Create an autonomous agent task."""
    return format_task("autonomous", task_type, kwargs.get("description", ""), **kwargs)


def filter_results_by_status(results: List[Dict[str, Any]], status: str) -> List[Dict[str, Any]]:
    """Filter results by status."""
    return [r for r in results if r.get("status") == status]


def get_completed_results(results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Get only completed results."""
    return filter_results_by_status(results, "completed")


def get_failed_results(results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Get only failed results."""
    return filter_results_by_status(results, "error")


def summarize_results(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Summarize a list of results."""
    total = len(results)
    completed = len(get_completed_results(results))
    failed = len(get_failed_results(results))

    return {
        "total": total,
        "completed": completed,
        "failed": failed,
        "success_rate": (completed / total * 100) if total > 0 else 0
    }


def export_to_csv(results: List[Dict[str, Any]], output_path: str) -> None:
    """Export results to CSV format."""
    import csv

    if not results:
        return

    keys = results[0].keys()

    with open(output_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(results)


def merge_configs(base_config: Dict[str, Any], override_config: Dict[str, Any]) -> Dict[str, Any]:
    """Merge two configuration dictionaries."""
    merged = base_config.copy()

    for key, value in override_config.items():
        if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
            merged[key] = merge_configs(merged[key], value)
        else:
            merged[key] = value

    return merged


class TaskBuilder:
    """Builder class for creating tasks with fluent interface."""

    def __init__(self):
        self._task = {}

    def agent(self, agent_type: str):
        """Set agent type."""
        self._task["agent_type"] = agent_type
        return self

    def type(self, task_type: str):
        """Set task type."""
        self._task["type"] = task_type
        return self

    def description(self, description: str):
        """Set description."""
        self._task["description"] = description
        return self

    def param(self, key: str, value: Any):
        """Add a parameter."""
        self._task[key] = value
        return self

    def params(self, **kwargs):
        """Add multiple parameters."""
        self._task.update(kwargs)
        return self

    def build(self) -> Dict[str, Any]:
        """Build and return the task."""
        self._task["timestamp"] = datetime.now().isoformat()
        return self._task.copy()
