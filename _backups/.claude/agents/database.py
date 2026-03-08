"""Database models and persistence layer for the multi-agent system."""

import json
import sqlite3
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
from contextlib import contextmanager


class Database:
    """SQLite database for persisting agent data."""

    def __init__(self, db_path: str = "agents.db"):
        self.db_path = db_path
        self.init_database()

    @contextmanager
    def get_connection(self):
        """Get a database connection context manager."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def init_database(self):
        """Initialize database tables."""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # Tasks table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    agent_type TEXT NOT NULL,
                    task_type TEXT NOT NULL,
                    description TEXT,
                    params TEXT,
                    status TEXT DEFAULT 'pending',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    started_at TIMESTAMP,
                    completed_at TIMESTAMP
                )
            """)

            # Results table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task_id INTEGER,
                    agent_type TEXT NOT NULL,
                    status TEXT NOT NULL,
                    message TEXT,
                    data TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (task_id) REFERENCES tasks (id)
                )
            """)

            # Agent states table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS agent_states (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    agent_type TEXT UNIQUE NOT NULL,
                    status TEXT NOT NULL,
                    queue_size INTEGER DEFAULT 0,
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Metrics table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    agent_type TEXT NOT NULL,
                    metric_name TEXT NOT NULL,
                    metric_value REAL NOT NULL,
                    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Goals table (for autonomous agent)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS goals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    description TEXT NOT NULL,
                    priority TEXT DEFAULT 'medium',
                    status TEXT DEFAULT 'active',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    completed_at TIMESTAMP
                )
            """)

    def save_task(self, task: Dict[str, Any]) -> int:
        """Save a task to the database."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO tasks (agent_type, task_type, description, params, status)
                VALUES (?, ?, ?, ?, ?)
            """, (
                task.get("agent_type"),
                task.get("type"),
                task.get("description"),
                json.dumps({k: v for k, v in task.items() if k not in ["agent_type", "type", "description"]}),
                "pending"
            ))
            return cursor.lastrowid

    def update_task_status(self, task_id: int, status: str, started_at: str = None, completed_at: str = None):
        """Update task status."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if started_at:
                cursor.execute("""
                    UPDATE tasks SET status = ?, started_at = ? WHERE id = ?
                """, (status, started_at, task_id))
            elif completed_at:
                cursor.execute("""
                    UPDATE tasks SET status = ?, completed_at = ? WHERE id = ?
                """, (status, completed_at, task_id))
            else:
                cursor.execute("""
                    UPDATE tasks SET status = ? WHERE id = ?
                """, (status, task_id))

    def save_result(self, result: Dict[str, Any], task_id: int = None):
        """Save a task result."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO results (task_id, agent_type, status, message, data)
                VALUES (?, ?, ?, ?, ?)
            """, (
                task_id,
                result.get("agent_type", "unknown"),
                result.get("status", "unknown"),
                result.get("message"),
                json.dumps(result)
            ))

    def get_tasks(self, agent_type: str = None, status: str = None, limit: int = 100) -> List[Dict[str, Any]]:
        """Get tasks from database."""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            query = "SELECT * FROM tasks WHERE 1=1"
            params = []

            if agent_type:
                query += " AND agent_type = ?"
                params.append(agent_type)

            if status:
                query += " AND status = ?"
                params.append(status)

            query += " ORDER BY created_at DESC LIMIT ?"
            params.append(limit)

            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]

    def get_results(self, agent_type: str = None, limit: int = 100) -> List[Dict[str, Any]]:
        """Get results from database."""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            query = "SELECT * FROM results WHERE 1=1"
            params = []

            if agent_type:
                query += " AND agent_type = ?"
                params.append(agent_type)

            query += " ORDER BY created_at DESC LIMIT ?"
            params.append(limit)

            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]

    def update_agent_state(self, agent_type: str, status: str, queue_size: int):
        """Update agent state."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO agent_states (agent_type, status, queue_size, last_updated)
                VALUES (?, ?, ?, CURRENT_TIMESTAMP)
            """, (agent_type, status, queue_size))

    def get_agent_states(self) -> List[Dict[str, Any]]:
        """Get all agent states."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM agent_states")
            return [dict(row) for row in cursor.fetchall()]

    def save_metric(self, agent_type: str, metric_name: str, metric_value: float):
        """Save a metric."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO metrics (agent_type, metric_name, metric_value)
                VALUES (?, ?, ?)
            """, (agent_type, metric_name, metric_value))

    def get_metrics(self, agent_type: str = None, metric_name: str = None, limit: int = 100) -> List[Dict[str, Any]]:
        """Get metrics from database."""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            query = "SELECT * FROM metrics WHERE 1=1"
            params = []

            if agent_type:
                query += " AND agent_type = ?"
                params.append(agent_type)

            if metric_name:
                query += " AND metric_name = ?"
                params.append(metric_name)

            query += " ORDER BY recorded_at DESC LIMIT ?"
            params.append(limit)

            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]

    def save_goal(self, goal: Dict[str, Any]) -> int:
        """Save a goal for autonomous agent."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO goals (description, priority, status)
                VALUES (?, ?, ?)
            """, (
                goal.get("description"),
                goal.get("priority", "medium"),
                goal.get("status", "active")
            ))
            return cursor.lastrowid

    def get_goals(self, status: str = None) -> List[Dict[str, Any]]:
        """Get goals from database."""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            if status:
                cursor.execute("SELECT * FROM goals WHERE status = ? ORDER BY created_at DESC", (status,))
            else:
                cursor.execute("SELECT * FROM goals ORDER BY created_at DESC")

            return [dict(row) for row in cursor.fetchall()]

    def complete_goal(self, goal_id: int):
        """Mark a goal as completed."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE goals SET status = 'completed', completed_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (goal_id,))

    def get_statistics(self) -> Dict[str, Any]:
        """Get overall statistics."""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # Total tasks
            cursor.execute("SELECT COUNT(*) as count FROM tasks")
            total_tasks = cursor.fetchone()["count"]

            # Completed tasks
            cursor.execute("SELECT COUNT(*) as count FROM tasks WHERE status = 'completed'")
            completed_tasks = cursor.fetchone()["count"]

            # Tasks by agent
            cursor.execute("""
                SELECT agent_type, COUNT(*) as count
                FROM tasks
                GROUP BY agent_type
            """)
            tasks_by_agent = {row["agent_type"]: row["count"] for row in cursor.fetchall()}

            # Success rate
            success_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0

            return {
                "total_tasks": total_tasks,
                "completed_tasks": completed_tasks,
                "success_rate": success_rate,
                "tasks_by_agent": tasks_by_agent
            }
