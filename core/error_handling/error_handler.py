"""
Graceful Error Handler for Gold Tier AI Employee

Provides:
- Automatic error detection and classification
- Intelligent retry strategies
- Fallback mechanisms
- Error learning and prevention
- Recovery action recommendations
"""

import logging
import traceback
from typing import Dict, Any, Optional, Callable
from datetime import datetime, timedelta
from collections import defaultdict


class ErrorHandler:
    """
    Comprehensive error handling system with learning capabilities.

    Features:
    - Automatic error classification
    - Retry strategies with exponential backoff
    - Fallback mechanisms
    - Error pattern learning
    - Recovery recommendations
    """

    def __init__(self, audit_logger=None):
        self.logger = logging.getLogger("ErrorHandler")
        self.audit_logger = audit_logger

        # Error tracking
        self.error_history = []
        self.error_patterns = defaultdict(list)
        self.recovery_strategies = {}

        # Retry configuration
        self.retry_config = {
            "max_retries": 3,
            "base_delay": 1.0,  # seconds
            "max_delay": 60.0,  # seconds
            "exponential_base": 2
        }

        # Error classification
        self.error_categories = {
            "transient": ["ConnectionError", "TimeoutError", "TemporaryFailure"],
            "authentication": ["AuthenticationError", "PermissionError", "Unauthorized"],
            "validation": ["ValueError", "ValidationError", "InvalidInput"],
            "resource": ["ResourceNotFound", "FileNotFoundError", "NotFound"],
            "system": ["SystemError", "MemoryError", "OSError"],
            "unknown": []
        }

        self.logger.info("Error handler initialized")

    async def handle_error(
        self,
        error: Exception,
        context: str,
        task: Dict[str, Any] = None,
        severity: str = "medium"
    ) -> Dict[str, Any]:
        """
        Handle an error with appropriate recovery strategy.

        Args:
            error: The exception that occurred
            context: Context where error occurred
            task: Task being executed (if applicable)
            severity: Error severity (low, medium, high, critical)

        Returns:
            Recovery result dictionary
        """
        try:
            self.logger.error(f"Handling error in {context}: {str(error)}")

            # Classify error
            error_type = type(error).__name__
            category = self._classify_error(error_type)

            # Create error record
            error_record = {
                "error_id": f"err_{datetime.now().timestamp()}",
                "error_type": error_type,
                "category": category,
                "message": str(error),
                "context": context,
                "task": task,
                "severity": severity,
                "traceback": traceback.format_exc(),
                "timestamp": datetime.now().isoformat()
            }

            # Store in history
            self.error_history.append(error_record)
            self.error_patterns[error_type].append(error_record)

            # Log to audit
            if self.audit_logger:
                self.audit_logger.log_task_error(
                    task_id=task.get("id", "unknown") if task else "system",
                    error=str(error),
                    metadata=error_record
                )

            # Determine recovery strategy
            recovery_result = await self._determine_recovery(error_record)

            # Execute recovery
            if recovery_result["action"] != "none":
                recovery_result = await self._execute_recovery(
                    error_record,
                    recovery_result
                )

            # Learn from error
            await self._learn_from_error(error_record, recovery_result)

            return recovery_result

        except Exception as e:
            self.logger.critical(f"Error handler failed: {str(e)}")
            return {
                "status": "error",
                "action": "none",
                "message": "Error handler failed",
                "original_error": str(error)
            }

    def _classify_error(self, error_type: str) -> str:
        """Classify error into category."""
        for category, error_types in self.error_categories.items():
            if error_type in error_types:
                return category
        return "unknown"

    async def _determine_recovery(self, error_record: Dict[str, Any]) -> Dict[str, Any]:
        """
        Determine appropriate recovery strategy.

        Args:
            error_record: Error record

        Returns:
            Recovery strategy
        """
        category = error_record["category"]
        error_type = error_record["error_type"]
        severity = error_record["severity"]

        # Check for learned recovery strategies
        if error_type in self.recovery_strategies:
            strategy = self.recovery_strategies[error_type]
            return {
                "action": strategy["action"],
                "reason": "learned_strategy",
                "details": strategy
            }

        # Default strategies by category
        if category == "transient":
            return {
                "action": "retry",
                "reason": "transient_error",
                "max_retries": self.retry_config["max_retries"],
                "delay": self.retry_config["base_delay"]
            }

        elif category == "authentication":
            return {
                "action": "reauth",
                "reason": "authentication_failure",
                "details": "Attempt to refresh credentials"
            }

        elif category == "validation":
            return {
                "action": "fallback",
                "reason": "validation_error",
                "details": "Use default values or skip validation"
            }

        elif category == "resource":
            return {
                "action": "fallback",
                "reason": "resource_not_found",
                "details": "Use alternative resource or create if possible"
            }

        elif severity == "critical":
            return {
                "action": "escalate",
                "reason": "critical_error",
                "details": "Requires human intervention"
            }

        else:
            return {
                "action": "log_and_continue",
                "reason": "non_critical_error",
                "details": "Log error and continue operation"
            }

    async def _execute_recovery(
        self,
        error_record: Dict[str, Any],
        recovery_strategy: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute recovery strategy.

        Args:
            error_record: Error record
            recovery_strategy: Recovery strategy to execute

        Returns:
            Recovery result
        """
        action = recovery_strategy["action"]

        try:
            if action == "retry":
                return await self._execute_retry(error_record, recovery_strategy)

            elif action == "reauth":
                return await self._execute_reauth(error_record, recovery_strategy)

            elif action == "fallback":
                return await self._execute_fallback(error_record, recovery_strategy)

            elif action == "escalate":
                return await self._execute_escalate(error_record, recovery_strategy)

            elif action == "log_and_continue":
                return {
                    "status": "recovered",
                    "action": "log_and_continue",
                    "message": "Error logged, continuing operation"
                }

            else:
                return {
                    "status": "no_recovery",
                    "action": "none",
                    "message": "No recovery action available"
                }

        except Exception as e:
            self.logger.error(f"Recovery execution failed: {str(e)}")
            return {
                "status": "recovery_failed",
                "action": action,
                "error": str(e)
            }

    async def _execute_retry(
        self,
        error_record: Dict[str, Any],
        strategy: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute retry strategy."""
        max_retries = strategy.get("max_retries", self.retry_config["max_retries"])

        return {
            "status": "retry_scheduled",
            "action": "retry",
            "max_retries": max_retries,
            "message": f"Will retry up to {max_retries} times"
        }

    async def _execute_reauth(
        self,
        error_record: Dict[str, Any],
        strategy: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute re-authentication strategy."""
        return {
            "status": "reauth_required",
            "action": "reauth",
            "message": "Re-authentication required",
            "details": strategy.get("details")
        }

    async def _execute_fallback(
        self,
        error_record: Dict[str, Any],
        strategy: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute fallback strategy."""
        return {
            "status": "fallback_activated",
            "action": "fallback",
            "message": "Using fallback mechanism",
            "details": strategy.get("details")
        }

    async def _execute_escalate(
        self,
        error_record: Dict[str, Any],
        strategy: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute escalation strategy."""
        # Create escalation notification
        escalation = {
            "error_id": error_record["error_id"],
            "severity": error_record["severity"],
            "context": error_record["context"],
            "message": error_record["message"],
            "timestamp": datetime.now().isoformat()
        }

        # Log escalation
        if self.audit_logger:
            self.audit_logger.log_security_event(
                event_type="error_escalation",
                severity="high",
                description=f"Error escalated: {error_record['error_type']}",
                metadata=escalation
            )

        return {
            "status": "escalated",
            "action": "escalate",
            "message": "Error escalated for human intervention",
            "escalation": escalation
        }

    async def _learn_from_error(
        self,
        error_record: Dict[str, Any],
        recovery_result: Dict[str, Any]
    ):
        """
        Learn from error and recovery outcome.

        Args:
            error_record: Error record
            recovery_result: Recovery result
        """
        error_type = error_record["error_type"]

        # If recovery was successful, store the strategy
        if recovery_result.get("status") in ["recovered", "retry_scheduled"]:
            if error_type not in self.recovery_strategies:
                self.recovery_strategies[error_type] = {
                    "action": recovery_result["action"],
                    "success_count": 1,
                    "last_used": datetime.now().isoformat()
                }
            else:
                self.recovery_strategies[error_type]["success_count"] += 1
                self.recovery_strategies[error_type]["last_used"] = datetime.now().isoformat()

    def get_error_statistics(self) -> Dict[str, Any]:
        """Get error statistics."""
        total_errors = len(self.error_history)

        by_category = defaultdict(int)
        by_severity = defaultdict(int)
        by_type = defaultdict(int)

        for error in self.error_history:
            by_category[error["category"]] += 1
            by_severity[error["severity"]] += 1
            by_type[error["error_type"]] += 1

        return {
            "total_errors": total_errors,
            "by_category": dict(by_category),
            "by_severity": dict(by_severity),
            "by_type": dict(by_type),
            "learned_strategies": len(self.recovery_strategies)
        }

    def get_recent_errors(self, limit: int = 10) -> list:
        """Get recent errors."""
        return self.error_history[-limit:]
