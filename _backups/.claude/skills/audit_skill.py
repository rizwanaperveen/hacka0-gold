"""Audit Skill - Comprehensive auditing and compliance tracking."""

import logging
import json
from typing import Dict, Any, List, Optional
from datetime import datetime
from pathlib import Path
import hashlib


class AuditSkill:
    """Skill for auditing, compliance tracking, and security monitoring."""

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.logger = logging.getLogger("AuditSkill")
        self.audit_log_file = config.get("audit_log_file", "logs/audit.log")
        self.audit_entries = []
        self.compliance_checks = []
        self.security_events = []
        self._setup_audit_log()

    def _setup_audit_log(self):
        """Setup audit log file."""
        log_path = Path(self.audit_log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

    def log_audit_event(
        self,
        event_type: str,
        actor: str,
        action: str,
        resource: str,
        result: str,
        details: Dict[str, Any] = None,
        ip_address: str = None
    ) -> Dict[str, Any]:
        """
        Log an audit event.

        Args:
            event_type: Type of event (access, modification, deletion, etc.)
            actor: User or system that performed the action
            action: Action performed
            resource: Resource affected
            result: Result of the action (success, failure, denied)
            details: Additional details
            ip_address: IP address of the actor

        Returns:
            Audit entry details
        """
        try:
            audit_entry = {
                "audit_id": self._generate_audit_id(),
                "event_type": event_type,
                "actor": actor,
                "action": action,
                "resource": resource,
                "result": result,
                "details": details or {},
                "ip_address": ip_address,
                "timestamp": datetime.now().isoformat(),
                "hash": None  # Will be set after creation
            }

            # Generate hash for integrity
            audit_entry["hash"] = self._generate_hash(audit_entry)

            self.audit_entries.append(audit_entry)

            # Write to audit log file
            self._write_to_audit_log(audit_entry)

            self.logger.info(
                f"Audit: {actor} performed {action} on {resource} - {result}"
            )

            return {
                "status": "success",
                "audit_id": audit_entry["audit_id"],
                "timestamp": audit_entry["timestamp"]
            }

        except Exception as e:
            self.logger.error(f"Failed to log audit event: {str(e)}")
            return {"status": "error", "error": str(e)}

    def log_access_event(
        self,
        user: str,
        resource: str,
        access_type: str,
        granted: bool,
        ip_address: str = None
    ) -> Dict[str, Any]:
        """
        Log an access event.

        Args:
            user: User attempting access
            resource: Resource being accessed
            access_type: Type of access (read, write, delete, etc.)
            granted: Whether access was granted
            ip_address: IP address

        Returns:
            Audit entry
        """
        return self.log_audit_event(
            event_type="access",
            actor=user,
            action=f"{access_type}_access",
            resource=resource,
            result="granted" if granted else "denied",
            ip_address=ip_address
        )

    def log_data_modification(
        self,
        user: str,
        resource: str,
        modification_type: str,
        old_value: Any = None,
        new_value: Any = None
    ) -> Dict[str, Any]:
        """
        Log a data modification event.

        Args:
            user: User making the modification
            resource: Resource being modified
            modification_type: Type of modification (create, update, delete)
            old_value: Previous value
            new_value: New value

        Returns:
            Audit entry
        """
        details = {
            "modification_type": modification_type,
            "old_value": str(old_value) if old_value else None,
            "new_value": str(new_value) if new_value else None
        }

        return self.log_audit_event(
            event_type="modification",
            actor=user,
            action=modification_type,
            resource=resource,
            result="success",
            details=details
        )

    def log_security_event(
        self,
        event_type: str,
        severity: str,
        description: str,
        source: str = None,
        details: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Log a security event.

        Args:
            event_type: Type of security event (intrusion, breach, suspicious_activity)
            severity: Severity level (low, medium, high, critical)
            description: Event description
            source: Source of the event
            details: Additional details

        Returns:
            Security event details
        """
        try:
            security_event = {
                "event_id": f"sec_{len(self.security_events) + 1}",
                "event_type": event_type,
                "severity": severity,
                "description": description,
                "source": source,
                "details": details or {},
                "timestamp": datetime.now().isoformat(),
                "resolved": False
            }

            self.security_events.append(security_event)

            # Also log as audit event
            self.log_audit_event(
                event_type="security",
                actor="system",
                action=event_type,
                resource=source or "system",
                result=severity,
                details=details
            )

            self.logger.warning(
                f"Security Event [{severity}]: {event_type} - {description}"
            )

            return {
                "status": "success",
                "event_id": security_event["event_id"],
                "severity": severity
            }

        except Exception as e:
            self.logger.error(f"Failed to log security event: {str(e)}")
            return {"status": "error", "error": str(e)}

    def perform_compliance_check(
        self,
        check_name: str,
        check_type: str,
        criteria: Dict[str, Any],
        result: bool,
        findings: List[str] = None
    ) -> Dict[str, Any]:
        """
        Record a compliance check.

        Args:
            check_name: Name of the compliance check
            check_type: Type of check (GDPR, HIPAA, SOC2, etc.)
            criteria: Criteria being checked
            result: Whether check passed
            findings: List of findings

        Returns:
            Compliance check details
        """
        try:
            compliance_check = {
                "check_id": f"comp_{len(self.compliance_checks) + 1}",
                "check_name": check_name,
                "check_type": check_type,
                "criteria": criteria,
                "result": "passed" if result else "failed",
                "findings": findings or [],
                "timestamp": datetime.now().isoformat()
            }

            self.compliance_checks.append(compliance_check)

            self.logger.info(
                f"Compliance Check: {check_name} ({check_type}) - {compliance_check['result']}"
            )

            return {
                "status": "success",
                "check_id": compliance_check["check_id"],
                "result": compliance_check["result"]
            }

        except Exception as e:
            self.logger.error(f"Failed to record compliance check: {str(e)}")
            return {"status": "error", "error": str(e)}

    def get_audit_trail(
        self,
        actor: str = None,
        resource: str = None,
        event_type: str = None,
        start_date: str = None,
        end_date: str = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Get audit trail with filters.

        Args:
            actor: Filter by actor
            resource: Filter by resource
            event_type: Filter by event type
            start_date: Start date (ISO format)
            end_date: End date (ISO format)
            limit: Maximum entries to return

        Returns:
            List of audit entries
        """
        filtered = self.audit_entries.copy()

        if actor:
            filtered = [e for e in filtered if e["actor"] == actor]
        if resource:
            filtered = [e for e in filtered if e["resource"] == resource]
        if event_type:
            filtered = [e for e in filtered if e["event_type"] == event_type]
        if start_date:
            filtered = [e for e in filtered if e["timestamp"] >= start_date]
        if end_date:
            filtered = [e for e in filtered if e["timestamp"] <= end_date]

        return filtered[-limit:]

    def get_security_events(
        self,
        severity: str = None,
        resolved: bool = None,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """Get security events with filters."""
        filtered = self.security_events.copy()

        if severity:
            filtered = [e for e in filtered if e["severity"] == severity]
        if resolved is not None:
            filtered = [e for e in filtered if e["resolved"] == resolved]

        return filtered[-limit:]

    def resolve_security_event(self, event_id: str, resolution: str) -> Dict[str, Any]:
        """Mark a security event as resolved."""
        for event in self.security_events:
            if event["event_id"] == event_id:
                event["resolved"] = True
                event["resolution"] = resolution
                event["resolved_at"] = datetime.now().isoformat()

                self.logger.info(f"Security event {event_id} resolved: {resolution}")

                return {"status": "success", "event_id": event_id}

        return {"status": "error", "error": "Event not found"}

    def get_compliance_report(self, check_type: str = None) -> Dict[str, Any]:
        """
        Generate a compliance report.

        Args:
            check_type: Filter by compliance type

        Returns:
            Compliance report
        """
        checks = self.compliance_checks

        if check_type:
            checks = [c for c in checks if c["check_type"] == check_type]

        total = len(checks)
        passed = len([c for c in checks if c["result"] == "passed"])
        failed = len([c for c in checks if c["result"] == "failed"])

        return {
            "total_checks": total,
            "passed": passed,
            "failed": failed,
            "compliance_rate": (passed / total * 100) if total > 0 else 0,
            "checks": checks
        }

    def verify_audit_integrity(self) -> Dict[str, Any]:
        """Verify the integrity of audit entries using hashes."""
        verified = 0
        tampered = []

        for entry in self.audit_entries:
            stored_hash = entry.get("hash")
            calculated_hash = self._generate_hash(entry)

            if stored_hash == calculated_hash:
                verified += 1
            else:
                tampered.append(entry["audit_id"])

        return {
            "total_entries": len(self.audit_entries),
            "verified": verified,
            "tampered": len(tampered),
            "tampered_ids": tampered,
            "integrity_status": "intact" if not tampered else "compromised"
        }

    def export_audit_report(
        self,
        output_file: str,
        include_security: bool = True,
        include_compliance: bool = True
    ) -> Dict[str, Any]:
        """Export comprehensive audit report."""
        try:
            report = {
                "generated_at": datetime.now().isoformat(),
                "audit_entries": self.audit_entries,
                "summary": {
                    "total_entries": len(self.audit_entries),
                    "by_event_type": self._count_by_field("event_type"),
                    "by_result": self._count_by_field("result")
                }
            }

            if include_security:
                report["security_events"] = self.security_events
                report["security_summary"] = {
                    "total_events": len(self.security_events),
                    "by_severity": self._count_security_by_severity(),
                    "unresolved": len([e for e in self.security_events if not e["resolved"]])
                }

            if include_compliance:
                report["compliance_checks"] = self.compliance_checks
                report["compliance_summary"] = self.get_compliance_report()

            with open(output_file, 'w') as f:
                json.dump(report, f, indent=2)

            self.logger.info(f"Audit report exported to {output_file}")

            return {"status": "success", "output_file": output_file}

        except Exception as e:
            self.logger.error(f"Failed to export audit report: {str(e)}")
            return {"status": "error", "error": str(e)}

    def _generate_audit_id(self) -> str:
        """Generate unique audit ID."""
        return f"audit_{datetime.now().timestamp()}_{len(self.audit_entries)}"

    def _generate_hash(self, entry: Dict[str, Any]) -> str:
        """Generate hash for audit entry integrity."""
        # Create a copy without the hash field
        entry_copy = {k: v for k, v in entry.items() if k != "hash"}
        entry_str = json.dumps(entry_copy, sort_keys=True)
        return hashlib.sha256(entry_str.encode()).hexdigest()

    def _write_to_audit_log(self, entry: Dict[str, Any]):
        """Write audit entry to log file."""
        try:
            with open(self.audit_log_file, 'a') as f:
                f.write(json.dumps(entry) + '\n')
        except Exception as e:
            self.logger.error(f"Failed to write to audit log: {str(e)}")

    def _count_by_field(self, field: str) -> Dict[str, int]:
        """Count audit entries by field."""
        counts = {}
        for entry in self.audit_entries:
            value = entry.get(field, "unknown")
            counts[value] = counts.get(value, 0) + 1
        return counts

    def _count_security_by_severity(self) -> Dict[str, int]:
        """Count security events by severity."""
        counts = {}
        for event in self.security_events:
            severity = event.get("severity", "unknown")
            counts[severity] = counts.get(severity, 0) + 1
        return counts


def example_usage():
    """Example usage of audit skill."""
    auditor = AuditSkill()

    # Log access event
    auditor.log_access_event(
        user="john.doe",
        resource="/api/users/123",
        access_type="read",
        granted=True,
        ip_address="192.168.1.100"
    )

    # Log data modification
    auditor.log_data_modification(
        user="admin",
        resource="user_profile",
        modification_type="update",
        old_value={"email": "old@example.com"},
        new_value={"email": "new@example.com"}
    )

    # Log security event
    auditor.log_security_event(
        event_type="suspicious_activity",
        severity="medium",
        description="Multiple failed login attempts",
        source="192.168.1.200",
        details={"attempts": 5, "user": "unknown"}
    )

    # Perform compliance check
    auditor.perform_compliance_check(
        check_name="Data Encryption Check",
        check_type="GDPR",
        criteria={"encryption": "AES-256", "at_rest": True},
        result=True
    )

    # Get audit trail
    trail = auditor.get_audit_trail(limit=10)
    print(f"Audit trail entries: {len(trail)}")

    # Verify integrity
    integrity = auditor.verify_audit_integrity()
    print(f"Audit integrity: {integrity['integrity_status']}")

    # Export report
    auditor.export_audit_report("logs/audit_report.json")


if __name__ == "__main__":
    example_usage()
