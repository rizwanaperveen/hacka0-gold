"""Autonomous Agent - Self-directed agent with independent decision-making."""

from typing import Any, Dict, List
from .base_agent import BaseAgent


class AutonomousAgent(BaseAgent):
    """Agent that operates independently with self-directed goals."""

    def __init__(self, config=None):
        super().__init__("Autonomous Agent", config)
        self.goals: List[Dict[str, Any]] = []
        self.actions_taken = []
        self.learning_data = []

    def set_goal(self, goal: Dict[str, Any]) -> None:
        """Set a goal for the autonomous agent."""
        self.goals.append(goal)
        self.logger.info(f"Goal set: {goal.get('description', 'No description')}")

    def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process a task autonomously."""
        task_type = task.get("type", "general")

        if task_type == "explore":
            return self._handle_exploration(task)
        elif task_type == "learn":
            return self._handle_learning(task)
        elif task_type == "optimize":
            return self._handle_optimization(task)
        elif task_type == "autonomous":
            return self._handle_autonomous_action(task)
        else:
            return {"status": "completed", "message": f"Processed autonomous task: {task.get('description')}"}

    def decide_action(self) -> Dict[str, Any]:
        """Decide next action based on current state and goals."""
        if not self.goals:
            return {"action": "idle", "reason": "No goals set"}

        current_goal = self.goals[0]
        action = {
            "goal": current_goal,
            "action": "work_towards_goal",
            "priority": current_goal.get("priority", "medium")
        }
        self.actions_taken.append(action)
        return action

    def _handle_exploration(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle exploration tasks."""
        area = task.get("area", "unknown")
        return {"status": "completed", "message": f"Explored: {area}"}

    def _handle_learning(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle learning tasks."""
        data = task.get("data", {})
        self.learning_data.append(data)
        return {"status": "completed", "message": f"Learned from data: {len(self.learning_data)} entries"}

    def _handle_optimization(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle optimization tasks."""
        target = task.get("target", "")
        return {"status": "completed", "message": f"Optimized: {target}"}

    def _handle_autonomous_action(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle fully autonomous actions."""
        action = self.decide_action()
        return {"status": "completed", "message": "Autonomous action taken", "action": action}

    def run(self) -> None:
        """Main execution loop with autonomous decision-making."""
        self.set_status("running")

        # Process queued tasks first
        while self.task_queue:
            task = self.task_queue.pop(0)
            try:
                result = self.process_task(task)
                self.results.append(result)
            except Exception as e:
                self.logger.error(f"Task failed: {str(e)}")

        # Then work on goals autonomously
        while self.goals:
            action = self.decide_action()
            if action["action"] == "idle":
                break

            # Simulate working towards goal
            goal = self.goals[0]
            if goal.get("completed", False):
                self.goals.pop(0)
                self.logger.info(f"Goal completed: {goal.get('description')}")

        self.set_status("idle")
