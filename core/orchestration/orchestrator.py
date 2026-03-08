"""
Core Orchestrator - Main system coordinator for Gold Tier AI Employee

This orchestrator manages:
- Task routing and delegation
- Cross-domain coordination (Personal + Business)
- Resource management
- State management
- Agent lifecycle
"""

import logging
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

from core.audit.audit_logger import AuditLogger
from core.error_handling.error_handler import ErrorHandler
from agents.coordinators.cross_domain_coordinator import CrossDomainCoordinator
from agents.coordinators.ceo_agent import CEOAgent


class CoreOrchestrator:
    """
    Main orchestrator for the autonomous AI employee system.

    Responsibilities:
    - Initialize and manage all agents
    - Route tasks to appropriate agents
    - Coordinate cross-domain operations
    - Manage system state
    - Handle errors gracefully
    - Maintain audit trail
    """

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or self._load_default_config()
        self.logger = logging.getLogger("CoreOrchestrator")

        # Initialize core systems
        self.audit_logger = AuditLogger(
            log_path=self.config.get("audit_log_path", "AI_Employee_Vault/logs/audit.log")
        )
        self.error_handler = ErrorHandler(
            audit_logger=self.audit_logger
        )

        # Initialize coordinators
        self.cross_domain_coordinator = CrossDomainCoordinator(
            audit_logger=self.audit_logger,
            error_handler=self.error_handler
        )
        self.ceo_agent = CEOAgent(
            audit_logger=self.audit_logger,
            error_handler=self.error_handler
        )

        # System state
        self.state = {
            "status": "initializing",
            "active_tasks": [],
            "completed_tasks": [],
            "errors": [],
            "start_time": datetime.now().isoformat()
        }

        # Agent registry
        self.agents = {}

        self.logger.info("Core Orchestrator initialized")
        self.audit_logger.log_system_event(
            event_type="system_start",
            description="Core Orchestrator initialized",
            metadata={"config": self.config}
        )

    def _load_default_config(self) -> Dict[str, Any]:
        """Load default configuration."""
        return {
            "environment": "production",
            "log_level": "INFO",
            "autonomous_mode": True,
            "audit_log_path": "AI_Employee_Vault/logs/audit.log",
            "data_path": "AI_Employee_Vault/data",
            "max_concurrent_tasks": 10,
            "domains": ["personal", "business", "social"],
            "mcp_servers": {
                "personal": {"host": "localhost", "port": 8001},
                "business": {"host": "localhost", "port": 8002},
                "social": {"host": "localhost", "port": 8003}
            }
        }

    async def initialize(self):
        """Initialize all system components."""
        try:
            self.logger.info("Initializing system components...")

            # Initialize agents
            await self._initialize_agents()

            # Initialize integrations
            await self._initialize_integrations()

            # Initialize MCP servers
            await self._initialize_mcp_servers()

            self.state["status"] = "ready"
            self.logger.info("System initialization complete")

            self.audit_logger.log_system_event(
                event_type="system_ready",
                description="All components initialized successfully"
            )

        except Exception as e:
            self.logger.error(f"Initialization failed: {str(e)}")
            self.state["status"] = "error"
            await self.error_handler.handle_error(
                error=e,
                context="system_initialization",
                severity="critical"
            )
            raise

    async def _initialize_agents(self):
        """Initialize all decision-making agents."""
        self.logger.info("Initializing agents...")

        # Import and initialize agents
        from agents.decision_makers.personal_agent import PersonalDecisionAgent
        from agents.decision_makers.business_agent import BusinessDecisionAgent
        from agents.decision_makers.social_agent import SocialDecisionAgent
        from agents.decision_makers.technical_agent import TechnicalDecisionAgent

        self.agents = {
            "personal": PersonalDecisionAgent(
                audit_logger=self.audit_logger,
                error_handler=self.error_handler
            ),
            "business": BusinessDecisionAgent(
                audit_logger=self.audit_logger,
                error_handler=self.error_handler
            ),
            "social": SocialDecisionAgent(
                audit_logger=self.audit_logger,
                error_handler=self.error_handler
            ),
            "technical": TechnicalDecisionAgent(
                audit_logger=self.audit_logger,
                error_handler=self.error_handler
            )
        }

        # Register agents with coordinators
        for agent_name, agent in self.agents.items():
            self.cross_domain_coordinator.register_agent(agent_name, agent)
            self.ceo_agent.register_agent(agent_name, agent)

        self.logger.info(f"Initialized {len(self.agents)} agents")

    async def _initialize_integrations(self):
        """Initialize external API integrations."""
        self.logger.info("Initializing integrations...")
        # Integration initialization will be handled by integration layer
        pass

    async def _initialize_mcp_servers(self):
        """Initialize MCP servers."""
        self.logger.info("Initializing MCP servers...")
        # MCP servers run independently, just verify connectivity
        pass

    async def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a task through the appropriate agent.

        Args:
            task: Task dictionary with type, domain, description, etc.

        Returns:
            Result dictionary with status and output
        """
        task_id = task.get("id", f"task_{datetime.now().timestamp()}")

        try:
            self.logger.info(f"Executing task: {task_id}")
            self.state["active_tasks"].append(task_id)

            # Log task start
            self.audit_logger.log_task_start(
                task_id=task_id,
                task_type=task.get("type"),
                domain=task.get("domain"),
                description=task.get("description")
            )

            # Determine routing
            domain = task.get("domain")
            cross_domain = task.get("cross_domain", False)

            # Route to appropriate handler
            if cross_domain:
                result = await self.cross_domain_coordinator.execute_task(task)
            elif domain in self.agents:
                result = await self.agents[domain].execute_task(task)
            else:
                # Route through CEO for complex decisions
                result = await self.ceo_agent.execute_task(task)

            # Log completion
            self.audit_logger.log_task_complete(
                task_id=task_id,
                status=result.get("status"),
                output=result.get("output")
            )

            self.state["active_tasks"].remove(task_id)
            self.state["completed_tasks"].append(task_id)

            return result

        except Exception as e:
            self.logger.error(f"Task execution failed: {str(e)}")

            # Handle error
            error_result = await self.error_handler.handle_error(
                error=e,
                context=f"task_execution_{task_id}",
                task=task
            )

            # Log error
            self.audit_logger.log_task_error(
                task_id=task_id,
                error=str(e),
                recovery_action=error_result.get("recovery_action")
            )

            if task_id in self.state["active_tasks"]:
                self.state["active_tasks"].remove(task_id)

            return {
                "status": "error",
                "error": str(e),
                "recovery": error_result
            }

    async def execute_batch(self, tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Execute multiple tasks concurrently."""
        self.logger.info(f"Executing batch of {len(tasks)} tasks")

        # Execute tasks concurrently with limit
        max_concurrent = self.config.get("max_concurrent_tasks", 10)
        results = []

        for i in range(0, len(tasks), max_concurrent):
            batch = tasks[i:i + max_concurrent]
            batch_results = await asyncio.gather(
                *[self.execute_task(task) for task in batch],
                return_exceptions=True
            )
            results.extend(batch_results)

        return results

    def get_status(self) -> Dict[str, Any]:
        """Get current system status."""
        return {
            "status": self.state["status"],
            "active_tasks": len(self.state["active_tasks"]),
            "completed_tasks": len(self.state["completed_tasks"]),
            "errors": len(self.state["errors"]),
            "uptime": (datetime.now() - datetime.fromisoformat(self.state["start_time"])).total_seconds(),
            "agents": {name: agent.get_status() for name, agent in self.agents.items()}
        }

    async def shutdown(self):
        """Gracefully shutdown the system."""
        self.logger.info("Shutting down system...")

        self.state["status"] = "shutting_down"

        # Wait for active tasks to complete
        while self.state["active_tasks"]:
            self.logger.info(f"Waiting for {len(self.state['active_tasks'])} active tasks...")
            await asyncio.sleep(1)

        # Shutdown agents
        for agent in self.agents.values():
            await agent.shutdown()

        # Log shutdown
        self.audit_logger.log_system_event(
            event_type="system_shutdown",
            description="System shutdown complete"
        )

        self.state["status"] = "stopped"
        self.logger.info("System shutdown complete")


async def main():
    """Main entry point for the orchestrator."""
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Create orchestrator
    orchestrator = CoreOrchestrator()

    try:
        # Initialize
        await orchestrator.initialize()

        # Example task
        task = {
            "id": "test_task_1",
            "type": "email_check",
            "domain": "personal",
            "description": "Check for important emails"
        }

        result = await orchestrator.execute_task(task)
        print(f"Task result: {result}")

        # Get status
        status = orchestrator.get_status()
        print(f"System status: {status}")

    except KeyboardInterrupt:
        print("\nShutdown requested...")
    finally:
        await orchestrator.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
