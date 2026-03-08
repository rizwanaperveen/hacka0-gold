"""Logging Skill - Advanced logging and monitoring capabilities."""

import logging
import json
from typing import Dict, Any, List, Optional
from datetime import datetime
from pathlib import Path
import traceback


class LoggingSkill:
    """Skill for advanced logging, monitoring, and event tracking."""

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.logger = logging.getLogger("LoggingSkill")
        self.log_file = config.get("log_file", "logs/application.log")
        self.log_level = config.get("log_level", "INFO")
        self.events = []
        self.errors = []
        self.metrics = {}
        self._setup_logging()

    def _setup_logging(self):
        """Setup logging configuration."""
        log_path = Path(self.log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        # Create file handler
        file_handler = logging.FileHandler(self.log_file)
        file_handler.setLevel(getattr(logging, self.log_level))

        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Configure root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(getattr(logging, self.log_level))
        root_logger.addHandler(file_handler)
        root_logger.addHandler(console_handler)

    def log_event(
        self,
        event_type: str,
        message: str,
        level: str = "info",
        metadata: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Log an event with metadata.

        Args:
            event_type: Type of event (user_action, system_event, api_call, etc.)
            message: Event message
            level: Log level (debug, info, warning, error, critical)
            metadata: Additional event metadata

        Returns:
            Logged event details
        """
        try:
            event = {
                "event_id": f"evt_{len(self.events) + 1}",
                "event_type": event_type,
                "message": message,
                "level": level,
                "metadata": metadata or {},
                "timestamp": datetime.now().isoformat()
            }

            self.events.append(event)

            # Log to standard logger
            log_method = getattr(self.logger, level.lower(), self.logger.info)
            log_method(f"[{event_type}] {message}")

            return {
                "status": "success",
                "event_id": event["event_id"],
                "logged_at": event["timestamp"]
            }

        except Exception as e:
            self.logger.error(f"Failed to log event: {str(e)}")
            return {"status": "error", "error": str(e)}

    def log_error(
        self,
        error: Exception,
        context: str = None,
        metadata: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Log an error with full traceback and context.

        Args:
            error: Exception object
            context: Context where error occurred
            metadata: Additional error metadata

        Returns:
            Logged error details
        """
        try:
            error_record = {
                "error_id": f"err_{len(self.errors) + 1}",
                "error_type": type(error).__name__,
                "error_message": str(error),
                "context": context,
                "traceback": traceback.format_exc(),
                "metadata": metadata or {},
                "timestamp": datetime.now().isoformat()
            }

            self.errors.append(error_record)

            # Log to standard logger
            self.logger.error(
                f"Error in {context}: {error_record['error_type']} - {error_record['error_message']}\n"
                f"{error_record['traceback']}"
            )

            return {
                "status": "success",
                "error_id": error_record["error_id"],
                "logged_at": error_record["timestamp"]
            }

        except Exception as e:
            self.logger.error(f"Failed to log error: {str(e)}")
            return {"status": "error", "error": str(e)}

    def log_metric(
        self,
        metric_name: str,
        value: float,
        unit: str = None,
        tags: Dict[str, str] = None
    ) -> Dict[str, Any]:
        """
        Log a metric value.

        Args:
            metric_name: Name of the metric
            value: Metric value
            unit: Unit of measurement
            tags: Additional tags for the metric

        Returns:
            Logged metric details
        """
        try:
            if metric_name not in self.metrics:
                self.metrics[metric_name] = []

            metric_record = {
                "value": value,
                "unit": unit,
                "tags": tags or {},
                "timestamp": datetime.now().isoformat()
            }

            self.metrics[metric_name].append(metric_record)

            self.logger.info(f"Metric: {metric_name} = {value} {unit or ''}")

            return {
                "status": "success",
                "metric_name": metric_name,
                "value": value
            }

        except Exception as e:
            self.logger.error(f"Failed to log metric: {str(e)}")
            return {"status": "error", "error": str(e)}

    def log_api_call(
        self,
        endpoint: str,
        method: str,
        status_code: int,
        duration_ms: float,
        request_data: Dict[str, Any] = None,
        response_data: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Log an API call with request/response details.

        Args:
            endpoint: API endpoint
            method: HTTP method
            status_code: Response status code
            duration_ms: Request duration in milliseconds
            request_data: Request payload
            response_data: Response payload

        Returns:
            Logged API call details
        """
        metadata = {
            "endpoint": endpoint,
            "method": method,
            "status_code": status_code,
            "duration_ms": duration_ms,
            "request_data": request_data,
            "response_data": response_data
        }

        return self.log_event(
            event_type="api_call",
            message=f"{method} {endpoint} - {status_code} ({duration_ms}ms)",
            level="info",
            metadata=metadata
        )

    def log_user_action(
        self,
        user_id: str,
        action: str,
        details: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Log a user action.

        Args:
            user_id: User identifier
            action: Action performed
            details: Action details

        Returns:
            Logged user action details
        """
        metadata = {
            "user_id": user_id,
            "action": action,
            "details": details or {}
        }

        return self.log_event(
            event_type="user_action",
            message=f"User {user_id} performed: {action}",
            level="info",
            metadata=metadata
        )

    def get_events(
        self,
        event_type: str = None,
        level: str = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Get logged events with optional filters.

        Args:
            event_type: Filter by event type
            level: Filter by log level
            limit: Maximum number of events to return

        Returns:
            List of events
        """
        filtered = self.events.copy()

        if event_type:
            filtered = [e for e in filtered if e["event_type"] == event_type]
        if level:
            filtered = [e for e in filtered if e["level"] == level]

        return filtered[-limit:]

    def get_errors(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent errors."""
        return self.errors[-limit:]

    def get_metrics(self, metric_name: str = None) -> Dict[str, Any]:
        """
        Get metrics data.

        Args:
            metric_name: Specific metric name, or None for all metrics

        Returns:
            Metrics data
        """
        if metric_name:
            return {metric_name: self.metrics.get(metric_name, [])}
        return self.metrics.copy()

    def get_metric_statistics(self, metric_name: str) -> Dict[str, Any]:
        """
        Get statistics for a specific metric.

        Args:
            metric_name: Metric name

        Returns:
            Statistics (min, max, avg, count)
        """
        if metric_name not in self.metrics:
            return {"status": "error", "error": "Metric not found"}

        values = [m["value"] for m in self.metrics[metric_name]]

        if not values:
            return {"status": "error", "error": "No data points"}

        return {
            "metric_name": metric_name,
            "count": len(values),
            "min": min(values),
            "max": max(values),
            "avg": sum(values) / len(values),
            "latest": values[-1]
        }

    def export_logs(
        self,
        output_file: str,
        format: str = "json",
        include_events: bool = True,
        include_errors: bool = True,
        include_metrics: bool = True
    ) -> Dict[str, Any]:
        """
        Export logs to a file.

        Args:
            output_file: Output file path
            format: Export format (json, csv)
            include_events: Include events
            include_errors: Include errors
            include_metrics: Include metrics

        Returns:
            Export result
        """
        try:
            export_data = {}

            if include_events:
                export_data["events"] = self.events
            if include_errors:
                export_data["errors"] = self.errors
            if include_metrics:
                export_data["metrics"] = self.metrics

            if format == "json":
                with open(output_file, 'w') as f:
                    json.dump(export_data, f, indent=2)
            else:
                return {"status": "error", "error": f"Format {format} not supported"}

            self.logger.info(f"Logs exported to {output_file}")

            return {
                "status": "success",
                "output_file": output_file,
                "format": format
            }

        except Exception as e:
            self.logger.error(f"Failed to export logs: {str(e)}")
            return {"status": "error", "error": str(e)}

    def clear_logs(self, clear_events: bool = True, clear_errors: bool = True, clear_metrics: bool = True):
        """Clear logged data."""
        if clear_events:
            self.events.clear()
        if clear_errors:
            self.errors.clear()
        if clear_metrics:
            self.metrics.clear()

        self.logger.info("Logs cleared")

    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of all logged data."""
        return {
            "total_events": len(self.events),
            "total_errors": len(self.errors),
            "total_metrics": len(self.metrics),
            "events_by_type": self._count_by_field(self.events, "event_type"),
            "events_by_level": self._count_by_field(self.events, "level"),
            "errors_by_type": self._count_by_field(self.errors, "error_type")
        }

    def _count_by_field(self, items: List[Dict], field: str) -> Dict[str, int]:
        """Count items by a specific field."""
        counts = {}
        for item in items:
            value = item.get(field, "unknown")
            counts[value] = counts.get(value, 0) + 1
        return counts


def example_usage():
    """Example usage of logging skill."""
    logger = LoggingSkill(config={"log_level": "INFO"})

    # Log an event
    logger.log_event(
        event_type="user_action",
        message="User logged in",
        level="info",
        metadata={"user_id": "user123", "ip": "192.168.1.1"}
    )

    # Log an error
    try:
        raise ValueError("Something went wrong")
    except Exception as e:
        logger.log_error(e, context="example_function")

    # Log metrics
    logger.log_metric("response_time", 145.5, unit="ms")
    logger.log_metric("active_users", 42, unit="count")

    # Log API call
    logger.log_api_call(
        endpoint="/api/users",
        method="GET",
        status_code=200,
        duration_ms=123.4
    )

    # Get summary
    summary = logger.get_summary()
    print(f"\nLog Summary: {json.dumps(summary, indent=2)}")

    # Export logs
    logger.export_logs("logs/export.json")


if __name__ == "__main__":
    example_usage()
