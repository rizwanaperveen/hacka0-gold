"""Skills Package - Specialized capabilities for the multi-agent system."""

from .gmail_skill import GmailSkill
from .summarization_skill import SummarizationSkill
from .social_post_skill import SocialPostSkill
from .task_creation_skill import TaskCreationSkill
from .logging_skill import LoggingSkill
from .audit_skill import AuditSkill

__all__ = [
    "GmailSkill",
    "SummarizationSkill",
    "SocialPostSkill",
    "TaskCreationSkill",
    "LoggingSkill",
    "AuditSkill",
]

__version__ = "1.0.0"
