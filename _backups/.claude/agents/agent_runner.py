"""Agent Runner - Main orchestrator for the multi-agent system."""

import logging
from typing import Dict, Any, List
from .ceo_agent import CEOAgent
from .personal_agent import PersonalAgent
from .business_agent import BusinessAgent
from .social_agent import SocialAgent
from .autonomous_agent import AutonomousAgent


class AgentRunner:
    """Main orchestrator for running and coordinating all agents."""

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.setup_logging()
        self.ceo = CEOAgent(config.get("ceo", {}))
        self.agents = self._initialize_agents()
        self._register_agents()

    def setup_logging(self) -> None:
        """Setup logging configuration."""
        log_level = self.config.get("log_level", "INFO")
        logging.basicConfig(
            level=getattr(logging, log_level),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

    def _initialize_agents(self) -> Dict[str, Any]:
        """Initialize all specialized agents."""
        return {
            "personal": PersonalAgent(self.config.get("personal", {})),
            "business": BusinessAgent(self.config.get("business", {})),
            "social": SocialAgent(self.config.get("social", {})),
            "autonomous": AutonomousAgent(self.config.get("autonomous", {}))
        }

    def _register_agents(self) -> None:
        """Register all agents with the CEO agent."""
        for agent in self.agents.values():
            self.ceo.register_agent(agent)

    def run_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Run a single task through the appropriate agent."""
        agent_type = task.get("agent_type", "ceo")

        if agent_type == "ceo":
            self.ceo.add_task(task)
            self.ceo.run()
            return self.ceo.get_results()[-1] if self.ceo.get_results() else {}

        agent = self.agents.get(agent_type)
        if agent:
            agent.add_task(task)
            agent.run()
            return agent.get_results()[-1] if agent.get_results() else {}

        return {"status": "error", "message": f"Unknown agent type: {agent_type}"}

    def run_batch(self, tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Run multiple tasks in batch."""
        results = []
        for task in tasks:
            result = self.run_task(task)
            results.append(result)
        return results

    def delegate_from_ceo(self, task: Dict[str, Any], target_agent: str) -> Dict[str, Any]:
        """Delegate a task from CEO to a specific agent."""
        delegation_task = {
            "type": "delegate",
            "agent": target_agent,
            "subtask": task,
            "description": f"Delegate to {target_agent}"
        }
        return self.run_task({"agent_type": "ceo", **delegation_task})

    def get_all_statuses(self) -> Dict[str, str]:
        """Get status of all agents."""
        statuses = {"ceo": self.ceo.get_status()}
        for name, agent in self.agents.items():
            statuses[name] = agent.get_status()
        return statuses

    def get_all_results(self) -> Dict[str, List[Dict[str, Any]]]:
        """Get results from all agents."""
        results = {"ceo": self.ceo.get_results()}
        for name, agent in self.agents.items():
            results[name] = agent.get_results()
        return results

    def clear_all_results(self) -> None:
        """Clear results from all agents."""
        self.ceo.clear_results()
        for agent in self.agents.values():
            agent.clear_results()


def main():
    """Example usage of the agent system."""
    # Initialize the agent runner
    config = {
        "log_level": "INFO",
        "ceo": {},
        "personal": {},
        "business": {},
        "social": {},
        "autonomous": {}
    }

    runner = AgentRunner(config)

    # Example tasks
    tasks = [
        {
            "agent_type": "personal",
            "type": "schedule",
            "event": {"title": "Team Meeting", "time": "10:00 AM"},
            "description": "Schedule team meeting"
        },
        {
            "agent_type": "business",
            "type": "analytics",
            "metric": "revenue",
            "value": 50000,
            "description": "Update revenue analytics"
        },
        {
            "agent_type": "social",
            "type": "post",
            "content": "Exciting product launch!",
            "platform": "twitter",
            "description": "Post to social media"
        }
    ]

    # Run tasks
    print("Running tasks...")
    results = runner.run_batch(tasks)

    # Display results
    print("\nResults:")
    for i, result in enumerate(results):
        print(f"Task {i+1}: {result}")

    # Check statuses
    print("\nAgent Statuses:")
    statuses = runner.get_all_statuses()
    for agent, status in statuses.items():
        print(f"{agent}: {status}")


if __name__ == "__main__":
    main()
