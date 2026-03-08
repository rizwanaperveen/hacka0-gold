"""
Core Layer - Gold Tier AI Employee

This package provides the core orchestration, autonomous loops,
audit logging, and error handling for the AI employee system.
"""

from core.orchestrator import CoreOrchestrator
from core.autonomous_loop.ralph_wiggum import RalphWiggumLoop
from core.audit.audit_logger import AuditLogger
from core.error_handling.error_handler import ErrorHandler
from core.reporting.weekly_briefing import WeeklyBriefingGenerator

__all__ = [
    "CoreOrchestrator",
    "RalphWiggumLoop",
    "AuditLogger",
    "ErrorHandler",
    "WeeklyBriefingGenerator",
]
