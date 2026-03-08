"""
Cross-Domain Coordinator - Integrates Personal + Business domains

This coordinator enables seamless integration between personal and business
activities, providing holistic context awareness and coordinated decision making.

Example: A business meeting reminder can trigger personal calendar updates,
travel arrangements, and preparation tasks across both domains.
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime


class CrossDomainCoordinator:
    """
    Coordinates activities across Personal and Business domains.

    Responsibilities:
    - Identify cross-domain dependencies
    - Coordinate multi-domain tasks
    - Maintain holistic context
    - Optimize resource allocation across domains
    """

    def __init__(self, audit_logger=None, error_handler=None):
        self.logger = logging.getLogger("CrossDomainCoordinator")
        self.audit_logger = audit_logger
        self.error_handler = error_handler

        # Agent registry
        self.agents = {}

        # Cross-domain context
        self.context = {
            "personal": {},
            "business": {},
            "shared": {}
        }

        # Active coordinations
        self.active_coordinations = []

        self.logger.info("Cross-domain coordinator initialized")

    def register_agent(self, domain: str, agent):
        """Register a domain agent."""
        self.agents[domain] = agent
        self.logger.info(f"Registered {domain} agent")

    async def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a cross-domain task.

        Args:
            task: Task with cross-domain requirements

        Returns:
            Execution result
        """
        try:
            task_id = task.get("id", f"cross_{datetime.now().timestamp()}")
            self.logger.info(f"Executing cross-domain task: {task_id}")

            # Analyze cross-domain dependencies
            dependencies = await self._analyze_dependencies(task)

            # Create coordination plan
            plan = await self._create_coordination_plan(task, dependencies)

            # Execute coordinated actions
            results = await self._execute_coordinated(plan)

            # Synthesize results
            final_result = await self._synthesize_results(results)

            if self.audit_logger:
                self.audit_logger.log_agent_action(
                    agent_name="CrossDomainCoordinator",
                    action="execute_task",
                    target=task_id,
                    result="success",
                    metadata={"dependencies": len(dependencies), "actions": len(results)}
                )

            return final_result

        except Exception as e:
            self.logger.error(f"Cross-domain execution failed: {str(e)}")

            if self.error_handler:
                return await self.error_handler.handle_error(
                    error=e,
                    context="cross_domain_execution",
                    task=task
                )

            return {"status": "error", "error": str(e)}

    async def _analyze_dependencies(self, task: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Analyze cross-domain dependencies.

        Args:
            task: Task to analyze

        Returns:
            List of dependencies
        """
        dependencies = []

        task_type = task.get("type")
        description = task.get("description", "")

        # Example: Meeting scheduling affects both personal and business
        if "meeting" in description.lower() or task_type == "schedule_meeting":
            dependencies.append({
                "domain": "personal",
                "action": "update_calendar",
                "reason": "Personal calendar needs meeting time blocked"
            })
            dependencies.append({
                "domain": "business",
                "action": "notify_participants",
                "reason": "Business contacts need meeting invitation"
            })

        # Example: Travel planning affects multiple domains
        if "travel" in description.lower() or task_type == "plan_travel":
            dependencies.append({
                "domain": "personal",
                "action": "arrange_transportation",
                "reason": "Personal travel arrangements needed"
            })
            dependencies.append({
                "domain": "business",
                "action": "update_availability",
                "reason": "Business calendar needs out-of-office"
            })

        # Example: Email response may need business context
        if task_type == "respond_email":
            # Check if email is business-related
            if task.get("metadata", {}).get("business_related"):
                dependencies.append({
                    "domain": "business",
                    "action": "get_context",
                    "reason": "Need business context for response"
                })

        return dependencies

    async def _create_coordination_plan(
        self,
        task: Dict[str, Any],
        dependencies: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Create a coordination plan for cross-domain execution.

        Args:
            task: Original task
            dependencies: Cross-domain dependencies

        Returns:
            Coordination plan
        """
        plan = {
            "task_id": task.get("id"),
            "primary_domain": task.get("domain", "personal"),
            "dependencies": dependencies,
            "execution_order": [],
            "parallel_actions": [],
            "sequential_actions": []
        }

        # Determine execution order
        # Some actions can run in parallel, others must be sequential
        for dep in dependencies:
            if dep.get("blocking", False):
                plan["sequential_actions"].append(dep)
            else:
                plan["parallel_actions"].append(dep)

        return plan

    async def _execute_coordinated(self, plan: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Execute coordinated actions across domains.

        Args:
            plan: Coordination plan

        Returns:
            List of action results
        """
        results = []

        # Execute sequential actions first
        for action in plan["sequential_actions"]:
            domain = action["domain"]
            if domain in self.agents:
                result = await self.agents[domain].execute_action(action)
                results.append(result)

        # Execute parallel actions
        # In a real implementation, these would run concurrently
        for action in plan["parallel_actions"]:
            domain = action["domain"]
            if domain in self.agents:
                result = await self.agents[domain].execute_action(action)
                results.append(result)

        return results

    async def _synthesize_results(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Synthesize results from multiple domains.

        Args:
            results: List of action results

        Returns:
            Synthesized result
        """
        # Check if all actions succeeded
        all_success = all(r.get("status") == "success" for r in results)

        return {
            "status": "success" if all_success else "partial_success",
            "cross_domain": True,
            "domain_results": results,
            "summary": f"Executed {len(results)} cross-domain actions"
        }

    def update_context(self, domain: str, context_data: Dict[str, Any]):
        """Update cross-domain context."""
        self.context[domain].update(context_data)

        # Update shared context
        self._update_shared_context()

    def _update_shared_context(self):
        """Update shared context from all domains."""
        # Merge relevant information from all domains
        self.context["shared"] = {
            "last_updated": datetime.now().isoformat(),
            "personal_summary": self._summarize_domain("personal"),
            "business_summary": self._summarize_domain("business")
        }

    def _summarize_domain(self, domain: str) -> Dict[str, Any]:
        """Summarize domain context."""
        domain_context = self.context.get(domain, {})

        return {
            "active_items": len(domain_context.get("active_items", [])),
            "pending_items": len(domain_context.get("pending_items", [])),
            "last_activity": domain_context.get("last_activity")
        }

    def get_status(self) -> Dict[str, Any]:
        """Get coordinator status."""
        return {
            "registered_agents": list(self.agents.keys()),
            "active_coordinations": len(self.active_coordinations),
            "context_domains": list(self.context.keys())
        }

    async def shutdown(self):
        """Shutdown coordinator."""
        self.logger.info("Shutting down cross-domain coordinator")
        self.active_coordinations.clear()
