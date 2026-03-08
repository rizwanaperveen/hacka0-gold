"""CEO Agent - Coordinates and oversees all other agents."""

from typing import Any, Dict, List, Optional
from .base_agent import BaseAgent


class CEOAgent(BaseAgent):
    """Agent for high-level coordination, strategy, and decision-making."""

    def __init__(self, config=None):
        super().__init__("CEO Agent", config)
        self.agents: List[BaseAgent] = []
        self.strategies = []
        self.delegations = []

    def register_agent(self, agent: BaseAgent) -> None:
        """Register a sub-agent to coordinate."""
        self.agents.append(agent)
        self.logger.info(f"Registered agent: {agent.name}")

    def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process a high-level task and coordinate agents."""
        task_type = task.get("type", "general")

        if task_type == "delegate":
            return self._handle_delegation(task)
        elif task_type == "strategy":
            return self._handle_strategy(task)
        elif task_type == "coordinate":
            return self._handle_coordination(task)
        elif task_type == "review":
            return self._handle_review(task)
        else:
            return {"status": "completed", "message": f"Processed CEO task: {task.get('description')}"}

    def _handle_delegation(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Delegate tasks to appropriate agents."""
        target_agent_name = task.get("agent", "")
        subtask = task.get("subtask", {})

        agent = self._find_agent(target_agent_name)
        if agent:
            agent.add_task(subtask)
            self.delegations.append({"agent": target_agent_name, "task": subtask})
            return {"status": "completed", "message": f"Delegated to {target_agent_name}"}
        else:
            return {"status": "error", "message": f"Agent not found: {target_agent_name}"}

    def _handle_strategy(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle strategic planning tasks."""
        strategy = task.get("strategy", {})
        self.strategies.append(strategy)
        return {"status": "completed", "message": f"Strategy planned: {strategy.get('name', 'Strategy')}"}

    def _handle_coordination(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Coordinate multiple agents for complex tasks."""
        agents_needed = task.get("agents", [])
        return {"status": "completed", "message": f"Coordinating {len(agents_needed)} agents"}

    def _handle_review(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Review agent performance and results."""
        results = []
        for agent in self.agents:
            results.append({"agent": agent.name, "status": agent.get_status()})
        return {"status": "completed", "message": "Review completed", "results": results}

    def _find_agent(self, name: str) -> Optional[BaseAgent]:
        """Find an agent by name."""
        for agent in self.agents:
            if agent.name.lower() == name.lower():
                return agent
        return None

    def delegate_task(self, task: Dict[str, Any], agent_name: str) -> None:
        """Delegate a task to a specific agent."""
        agent = self._find_agent(agent_name)
        if agent:
            agent.add_task(task)
            self.logger.info(f"Task delegated to {agent_name}")
        else:
            self.logger.error(f"Agent not found: {agent_name}")
