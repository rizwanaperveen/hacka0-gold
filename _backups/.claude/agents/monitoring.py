"""Monitoring and metrics for the multi-agent system."""

import time
from typing import Dict, Any, List
from datetime import datetime
from collections import defaultdict


class AgentMetrics:
    """Collect and track metrics for agent performance."""

    def __init__(self):
        self.task_counts = defaultdict(int)
        self.task_durations = defaultdict(list)
        self.task_statuses = defaultdict(lambda: defaultdict(int))
        self.agent_activity = defaultdict(list)
        self.start_time = time.time()

    def record_task_start(self, agent_type: str, task_id: str) -> float:
        """Record when a task starts."""
        start_time = time.time()
        self.agent_activity[agent_type].append({
            "task_id": task_id,
            "start_time": start_time,
            "timestamp": datetime.now().isoformat()
        })
        return start_time

    def record_task_complete(self, agent_type: str, task_id: str, start_time: float, status: str) -> None:
        """Record when a task completes."""
        duration = time.time() - start_time

        self.task_counts[agent_type] += 1
        self.task_durations[agent_type].append(duration)
        self.task_statuses[agent_type][status] += 1

    def get_agent_stats(self, agent_type: str) -> Dict[str, Any]:
        """Get statistics for a specific agent."""
        durations = self.task_durations[agent_type]

        if not durations:
            return {
                "agent": agent_type,
                "total_tasks": 0,
                "avg_duration": 0,
                "min_duration": 0,
                "max_duration": 0,
                "statuses": dict(self.task_statuses[agent_type])
            }

        return {
            "agent": agent_type,
            "total_tasks": self.task_counts[agent_type],
            "avg_duration": sum(durations) / len(durations),
            "min_duration": min(durations),
            "max_duration": max(durations),
            "statuses": dict(self.task_statuses[agent_type])
        }

    def get_all_stats(self) -> Dict[str, Any]:
        """Get statistics for all agents."""
        stats = {}
        for agent_type in self.task_counts.keys():
            stats[agent_type] = self.get_agent_stats(agent_type)

        return {
            "agents": stats,
            "uptime": time.time() - self.start_time,
            "total_tasks": sum(self.task_counts.values())
        }

    def get_success_rate(self, agent_type: str) -> float:
        """Get success rate for an agent."""
        statuses = self.task_statuses[agent_type]
        total = sum(statuses.values())

        if total == 0:
            return 0.0

        completed = statuses.get("completed", 0)
        return (completed / total) * 100

    def reset(self) -> None:
        """Reset all metrics."""
        self.task_counts.clear()
        self.task_durations.clear()
        self.task_statuses.clear()
        self.agent_activity.clear()
        self.start_time = time.time()


class PerformanceMonitor:
    """Monitor system performance and health."""

    def __init__(self):
        self.metrics = AgentMetrics()
        self.alerts = []
        self.thresholds = {
            "max_duration": 10.0,  # seconds
            "min_success_rate": 80.0,  # percentage
            "max_queue_size": 100
        }

    def check_health(self, runner) -> Dict[str, Any]:
        """Check overall system health."""
        health = {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "agents": {},
            "alerts": []
        }

        # Check each agent
        for agent_name, agent in runner.agents.items():
            agent_health = {
                "status": agent.get_status(),
                "queue_size": len(agent.task_queue),
                "results_count": len(agent.results)
            }

            # Check queue size
            if agent_health["queue_size"] > self.thresholds["max_queue_size"]:
                alert = f"{agent_name} queue size exceeds threshold: {agent_health['queue_size']}"
                health["alerts"].append(alert)
                health["status"] = "warning"

            health["agents"][agent_name] = agent_health

        # Check success rates
        for agent_type in runner.agents.keys():
            success_rate = self.metrics.get_success_rate(agent_type)
            if success_rate > 0 and success_rate < self.thresholds["min_success_rate"]:
                alert = f"{agent_type} success rate below threshold: {success_rate:.1f}%"
                health["alerts"].append(alert)
                health["status"] = "warning"

        return health

    def get_performance_report(self) -> Dict[str, Any]:
        """Generate a performance report."""
        stats = self.metrics.get_all_stats()

        report = {
            "timestamp": datetime.now().isoformat(),
            "uptime": stats["uptime"],
            "total_tasks": stats["total_tasks"],
            "agents": {}
        }

        for agent_type, agent_stats in stats["agents"].items():
            report["agents"][agent_type] = {
                **agent_stats,
                "success_rate": self.metrics.get_success_rate(agent_type)
            }

        return report

    def set_threshold(self, key: str, value: float) -> None:
        """Set a performance threshold."""
        self.thresholds[key] = value

    def get_alerts(self) -> List[str]:
        """Get all active alerts."""
        return self.alerts.copy()

    def clear_alerts(self) -> None:
        """Clear all alerts."""
        self.alerts.clear()


def create_dashboard_data(runner, monitor: PerformanceMonitor) -> Dict[str, Any]:
    """Create data for a monitoring dashboard."""
    health = monitor.check_health(runner)
    performance = monitor.get_performance_report()
    statuses = runner.get_all_statuses()

    return {
        "timestamp": datetime.now().isoformat(),
        "health": health,
        "performance": performance,
        "statuses": statuses,
        "metrics": monitor.metrics.get_all_stats()
    }
