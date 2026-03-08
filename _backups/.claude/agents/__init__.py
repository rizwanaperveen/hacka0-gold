"""
Multi-Agent System Package

A flexible multi-agent system for task automation and coordination.
"""

__version__ = "1.0.0"
__author__ = "Multi-Agent System Team"
__license__ = "MIT"

from .base_agent import BaseAgent
from .personal_agent import PersonalAgent
from .business_agent import BusinessAgent
from .social_agent import SocialAgent
from .ceo_agent import CEOAgent
from .autonomous_agent import AutonomousAgent
from .agent_runner import AgentRunner

__all__ = [
    "BaseAgent",
    "PersonalAgent",
    "BusinessAgent",
    "SocialAgent",
    "CEOAgent",
    "AutonomousAgent",
    "AgentRunner",
]
