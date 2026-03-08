"""Diagnostics and health check utilities."""

import sys
import time
import psutil
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime


class SystemDiagnostics:
    """System diagnostics and health checks."""

    def __init__(self):
        self.checks = []
        self.results = []

    def add_check(self, name: str, check_func: callable) -> None:
        """Add a diagnostic check."""
        self.checks.append({"name": name, "func": check_func})

    def run_all_checks(self) -> Dict[str, Any]:
        """Run all diagnostic checks."""
        self.results = []
        start_time = time.time()

        for check in self.checks:
            result = self._run_check(check)
            self.results.append(result)

        duration = time.time() - start_time

        return {
            "timestamp": datetime.now().isoformat(),
            "duration": duration,
            "checks": self.results,
            "passed": sum(1 for r in self.results if r["status"] == "pass"),
            "failed": sum(1 for r in self.results if r["status"] == "fail"),
            "warnings": sum(1 for r in self.results if r["status"] == "warning")
        }

    def _run_check(self, check: Dict[str, Any]) -> Dict[str, Any]:
        """Run a single diagnostic check."""
        try:
            start = time.time()
            status, message = check["func"]()
            duration = time.time() - start

            return {
                "name": check["name"],
                "status": status,
                "message": message,
                "duration": duration
            }
        except Exception as e:
            return {
                "name": check["name"],
                "status": "fail",
                "message": f"Check failed: {str(e)}",
                "duration": 0
            }

    def print_report(self) -> None:
        """Print diagnostic report."""
        report = self.run_all_checks()

        print("\n" + "=" * 60)
        print("System Diagnostics Report")
        print("=" * 60)
        print(f"Timestamp: {report['timestamp']}")
        print(f"Duration: {report['duration']:.2f}s")
        print()

        for check in report["checks"]:
            status_icon = {
                "pass": "✓",
                "fail": "✗",
                "warning": "⚠"
            }.get(check["status"], "?")

            print(f"{status_icon} {check['name']}")
            print(f"  Status: {check['status'].upper()}")
            print(f"  Message: {check['message']}")
            print(f"  Duration: {check['duration']:.3f}s")
            print()

        print("-" * 60)
        print(f"Summary: {report['passed']} passed, {report['failed']} failed, {report['warnings']} warnings")
        print("=" * 60)


def check_python_version() -> tuple:
    """Check Python version."""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        return "pass", f"Python {version.major}.{version.minor}.{version.micro}"
    else:
        return "fail", f"Python {version.major}.{version.minor} (requires 3.8+)"


def check_dependencies() -> tuple:
    """Check required dependencies."""
    required = ["flask", "flask_cors"]
    missing = []

    for module in required:
        try:
            __import__(module)
        except ImportError:
            missing.append(module)

    if not missing:
        return "pass", "All dependencies installed"
    else:
        return "fail", f"Missing: {', '.join(missing)}"


def check_config_files() -> tuple:
    """Check configuration files."""
    required_files = ["config.json"]
    optional_files = [".env"]

    missing_required = [f for f in required_files if not Path(f).exists()]
    missing_optional = [f for f in optional_files if not Path(f).exists()]

    if missing_required:
        return "fail", f"Missing required files: {', '.join(missing_required)}"
    elif missing_optional:
        return "warning", f"Missing optional files: {', '.join(missing_optional)}"
    else:
        return "pass", "All configuration files present"


def check_directories() -> tuple:
    """Check required directories."""
    required_dirs = ["data", "logs"]
    missing = [d for d in required_dirs if not Path(d).exists()]

    if missing:
        return "warning", f"Missing directories: {', '.join(missing)}"
    else:
        return "pass", "All directories present"


def check_agent_imports() -> tuple:
    """Check if agents can be imported."""
    try:
        from agent_runner import AgentRunner
        from base_agent import BaseAgent
        from personal_agent import PersonalAgent
        from business_agent import BusinessAgent
        from social_agent import SocialAgent
        from ceo_agent import CEOAgent
        from autonomous_agent import AutonomousAgent

        return "pass", "All agents can be imported"
    except ImportError as e:
        return "fail", f"Import error: {str(e)}"


def check_system_resources() -> tuple:
    """Check system resources."""
    try:
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('.')

        issues = []

        if cpu_percent > 90:
            issues.append(f"High CPU usage: {cpu_percent}%")

        if memory.percent > 90:
            issues.append(f"High memory usage: {memory.percent}%")

        if disk.percent > 90:
            issues.append(f"High disk usage: {disk.percent}%")

        if issues:
            return "warning", "; ".join(issues)
        else:
            return "pass", f"CPU: {cpu_percent}%, Memory: {memory.percent}%, Disk: {disk.percent}%"

    except Exception as e:
        return "warning", f"Could not check resources: {str(e)}"


def check_database() -> tuple:
    """Check database connectivity."""
    try:
        from database import Database

        db = Database("agents.db")
        stats = db.get_statistics()

        return "pass", f"Database OK ({stats['total_tasks']} tasks)"
    except Exception as e:
        return "warning", f"Database check failed: {str(e)}"


def check_api_server() -> tuple:
    """Check if API server is running."""
    try:
        import requests
        response = requests.get("http://localhost:5000/health", timeout=2)

        if response.status_code == 200:
            return "pass", "API server is running"
        else:
            return "warning", f"API server returned status {response.status_code}"

    except requests.exceptions.ConnectionError:
        return "warning", "API server is not running"
    except Exception as e:
        return "warning", f"Could not check API server: {str(e)}"


def run_diagnostics():
    """Run full system diagnostics."""
    diagnostics = SystemDiagnostics()

    # Add checks
    diagnostics.add_check("Python Version", check_python_version)
    diagnostics.add_check("Dependencies", check_dependencies)
    diagnostics.add_check("Configuration Files", check_config_files)
    diagnostics.add_check("Directories", check_directories)
    diagnostics.add_check("Agent Imports", check_agent_imports)
    diagnostics.add_check("System Resources", check_system_resources)
    diagnostics.add_check("Database", check_database)
    diagnostics.add_check("API Server", check_api_server)

    # Run and print report
    diagnostics.print_report()


if __name__ == "__main__":
    run_diagnostics()
