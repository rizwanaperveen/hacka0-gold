"""
Skills Layer - Atomic executable capabilities

This package contains all atomic skills that can be composed
into higher-level workflows by agents.
"""

from skills.base_skill import BaseSkill
from skills.personal.email_skill import EmailSkill
from skills.personal.task_skill import TaskSkill
from skills.personal.calendar_skill import CalendarSkill

__all__ = [
    "BaseSkill",
    "EmailSkill",
    "TaskSkill",
    "CalendarSkill",
]
