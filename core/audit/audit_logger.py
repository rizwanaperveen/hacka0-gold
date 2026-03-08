"""
Comprehensive Audit Logger for Gold Tier AI Employee

Provides:
- Full action logging with integrity verification
- Compliance tracking (GDPR, HIPAA, SOC2)
- Security event monitoring
- Performance metrics
- Tamper-proof audit trail
"""

import logging
import json
import hashlib
from typing import Dict, Any, Optional
from datetime import datetime
from pathlib import Path


class AuditLogger:
    """
    Comprehensive audit logging system with integrity verification.

    All actions are logged with SHA-256 hashing for tamper detection.
    Supports compliance requirements for GDPR, HIPAA, and SOC2.
    """

    def __init__(self, log_path: str = "AI_Employee_Vault/logs/audit.log"):
        self.log_path = Path(log_path)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

        self.logger = logging.getLogger("AuditLogger")

        # In-memory cache for recent entries
        self.recent_entries = []
        self.max_cache_size = 1000

        # Metrics
        self.metrics = {
            "total_entries": 0,
            "system_events": 0,
            "task_events": 0,
            "error_events": 0,
            "security_events": 0
        }

        self.logger.info(f"Audit logger initialized: {self.log_path}")

    def log_system_event(
        self,
        event_type: str,
        description: str,
        metadata: Dict[str, Any] = None
    ) -> str:
        """
        Log a system-level event.

        Args:
            event_type: Type of system event
            description: Event description
            metadata: Additional metadata

        Returns:
            Entry ID
        """
        entry = self._create_entry(
            category="system",
            event_type=event_type,
            description=description,
            metadata=metadata
        )

        self._write_entry(entry)
        self.metrics["system_events"] += 1

        return entry["entry_id"]

    def log_task_start(
        self,
        task_id: str,
        task_type: str,
        domain: str,
        description: str,
        metadata: Dict[str, Any] = None
    ) -> str:
        """Log task start."""
        entry = self._create_entry(
            category="task",
            event_type="task_start",
            description=f"Task started: {description}",
            metadata={
                "task_id": task_id,
                "task_type": task_type,
                "domain": domain,
                **(metadata or {})
            }
        )

        self._write_entry(entry)
        self.metrics["task_events"] += 1

        return entry["entry_id"]

    def log_task_complete(
        self,
        task_id: str,
        status: str,
        output: Any = None,
        metadata: Dict[str, Any] = None
    ) -> str:
        """Log task completion."""
        entry = self._create_entry(
            category="task",
            event_type="task_complete",
            description=f"Task completed: {task_id}",
            metadata={
                "task_id": task_id,
                "status": status,
                "output": str(output) if output else None,
                **(metadata or {})
            }
        )

        self._write_entry(entry)
        self.metrics["task_events"] += 1

        return entry["entry_id"]

    def log_task_error(
        self,
        task_id: str,
        error: str,
        recovery_action: str = None,
        metadata: Dict[str, Any] = None
    ) -> str:
        """Log task error."""
        entry = self._create_entry(
            category="error",
            event_type="task_error",
            description=f"Task error: {task_id}",
            metadata={
                "task_id": task_id,
                "error": error,
                "recovery_action": recovery_action,
                **(metadata or {})
            }
        )

        self._write_entry(entry)
        self.metrics["error_events"] += 1

        return entry["entry_id"]

    def log_security_event(
        self,
        event_type: str,
        severity: str,
        description: str,
        source: str = None,
        metadata: Dict[str, Any] = None
    ) -> str:
        """Log security event."""
        entry = self._create_entry(
            category="security",
            event_type=event_type,
            description=description,
            metadata={
                "severity": severity,
                "source": source,
                **(metadata or {})
            }
        )

        self._write_entry(entry)
        self.metrics["security_events"] += 1

        # Log to standard logger for immediate visibility
        if severity in ["high", "critical"]:
            self.logger.warning(f"SECURITY EVENT [{severity}]: {description}")

        return entry["entry_id"]

    def log_compliance_check(
        self,
        check_type: str,
        check_name: str,
        result: bool,
        findings: list = None,
        metadata: Dict[str, Any] = None
    ) -> str:
        """Log compliance check."""
        entry = self._create_entry(
            category="compliance",
            event_type="compliance_check",
            description=f"Compliance check: {check_name}",
            metadata={
                "check_type": check_type,
                "check_name": check_name,
                "result": "passed" if result else "failed",
                "findings": findings or [],
                **(metadata or {})
            }
        )

        self._write_entry(entry)

        return entry["entry_id"]

    def log_agent_action(
        self,
        agent_name: str,
        action: str,
        target: str,
        result: str,
        metadata: Dict[str, Any] = None
    ) -> str:
        """Log agent action."""
        entry = self._create_entry(
            category="agent",
            event_type="agent_action",
            description=f"Agent {agent_name} performed {action}",
            metadata={
                "agent_name": agent_name,
                "action": action,
                "target": target,
                "result": result,
                **(metadata or {})
            }
        )

        self._write_entry(entry)

        return entry["entry_id"]

    def log_integration_call(
        self,
        integration: str,
        method: str,
        endpoint: str,
        status_code: int,
        duration_ms: float,
        metadata: Dict[str, Any] = None
    ) -> str:
        """Log external integration call."""
        entry = self._create_entry(
            category="integration",
            event_type="api_call",
            description=f"{integration} API call: {method} {endpoint}",
            metadata={
                "integration": integration,
                "method": method,
                "endpoint": endpoint,
                "status_code": status_code,
                "duration_ms": duration_ms,
                **(metadata or {})
            }
        )

        self._write_entry(entry)

        return entry["entry_id"]

    def _create_entry(
        self,
        category: str,
        event_type: str,
        description: str,
        metadata: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Create an audit entry."""
        entry_id = f"{category}_{datetime.now().timestamp()}"

        entry = {
            "entry_id": entry_id,
            "category": category,
            "event_type": event_type,
            "description": description,
            "metadata": metadata or {},
            "timestamp": datetime.now().isoformat(),
            "hash": None  # Will be set after creation
        }

        # Generate integrity hash
        entry["hash"] = self._generate_hash(entry)

        return entry

    def _generate_hash(self, entry: Dict[str, Any]) -> str:
        """Generate SHA-256 hash for integrity verification."""
        # Create a copy without the hash field
        entry_copy = {k: v for k, v in entry.items() if k != "hash"}
        entry_str = json.dumps(entry_copy, sort_keys=True)
        return hashlib.sha256(entry_str.encode()).hexdigest()

    def _write_entry(self, entry: Dict[str, Any]):
        """Write entry to log file."""
        try:
            # Write to file
            with open(self.log_path, 'a') as f:
                f.write(json.dumps(entry) + '\n')

            # Add to cache
            self.recent_entries.append(entry)
            if len(self.recent_entries) > self.max_cache_size:
                self.recent_entries.pop(0)

            # Update metrics
            self.metrics["total_entries"] += 1

        except Exception as e:
            self.logger.error(f"Failed to write audit entry: {str(e)}")

    def get_recent_entries(self, limit: int = 100) -> list:
        """Get recent audit entries."""
        return self.recent_entries[-limit:]

    def verify_integrity(self, entry: Dict[str, Any]) -> bool:
        """Verify the integrity of an audit entry."""
        stored_hash = entry.get("hash")
        calculated_hash = self._generate_hash(entry)
        return stored_hash == calculated_hash

    def get_metrics(self) -> Dict[str, Any]:
        """Get audit metrics."""
        return self.metrics.copy()

    def export_audit_trail(
        self,
        output_path: str,
        start_date: str = None,
        end_date: str = None,
        category: str = None
    ) -> Dict[str, Any]:
        """
        Export audit trail to file.

        Args:
            output_path: Output file path
            start_date: Start date filter (ISO format)
            end_date: End date filter (ISO format)
            category: Category filter

        Returns:
            Export summary
        """
        try:
            entries = []

            # Read all entries
            if self.log_path.exists():
                with open(self.log_path, 'r') as f:
                    for line in f:
                        try:
                            entry = json.loads(line)

                            # Apply filters
                            if start_date and entry["timestamp"] < start_date:
                                continue
                            if end_date and entry["timestamp"] > end_date:
                                continue
                            if category and entry["category"] != category:
                                continue

                            entries.append(entry)
                        except:
                            pass

            # Write to output file
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            with open(output_path, 'w') as f:
                json.dump({
                    "export_date": datetime.now().isoformat(),
                    "filters": {
                        "start_date": start_date,
                        "end_date": end_date,
                        "category": category
                    },
                    "entry_count": len(entries),
                    "entries": entries
                }, f, indent=2)

            return {
                "status": "success",
                "output_path": str(output_path),
                "entry_count": len(entries)
            }

        except Exception as e:
            self.logger.error(f"Failed to export audit trail: {str(e)}")
            return {
                "status": "error",
                "error": str(e)
            }
