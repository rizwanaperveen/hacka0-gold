"""
Configuration Management - Gold Tier AI Employee

Provides centralized configuration management for:
- System settings
- Domain configurations
- MCP server settings
- Integration credentials
- Audit logging settings
"""

import os
import json
import logging
from typing import Dict, Any, Optional
from pathlib import Path
from datetime import datetime

from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """
    Centralized configuration management.

    Loads configuration from:
    1. Environment variables
    2. .env file
    3. Default values
    """

    def __init__(self, config_path: str = None):
        self.config_path = Path(config_path) if config_path else None
        self.logger = logging.getLogger("Config")

        # Load configuration
        self.config = self._load_config()

        self.logger.info("Configuration loaded")

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from all sources."""
        config = {
            # System settings
            "environment": os.getenv("ENVIRONMENT", "production"),
            "log_level": os.getenv("LOG_LEVEL", "INFO"),
            "debug": os.getenv("DEBUG", "false").lower() == "true",

            # Vault configuration
            "vault_path": os.getenv("VAULT_PATH", "AI_Employee_Vault"),

            # Watcher configuration
            "gmail_check_interval": int(os.getenv("GMAIL_CHECK_INTERVAL", "120")),
            "whatsapp_check_interval": int(os.getenv("WHATSAPP_CHECK_INTERVAL", "30")),
            "linkedin_check_interval": int(os.getenv("LINKEDIN_CHECK_INTERVAL", "300")),

            # Security
            "dry_run": os.getenv("DRY_RUN", "false").lower() == "true",

            # Domains
            "domains": ["personal", "business", "social", "technical"],

            # MCP servers
            "mcp_servers": {
                "personal": {
                    "host": os.getenv("PERSONAL_MCP_HOST", "localhost"),
                    "port": int(os.getenv("PERSONAL_MCP_PORT", "8001"))
                },
                "business": {
                    "host": os.getenv("BUSINESS_MCP_HOST", "localhost"),
                    "port": int(os.getenv("BUSINESS_MCP_PORT", "8002"))
                },
                "social": {
                    "host": os.getenv("SOCIAL_MCP_HOST", "localhost"),
                    "port": int(os.getenv("SOCIAL_MCP_PORT", "8003"))
                }
            },

            # Autonomous loop configuration
            "autonomous_loop": {
                "enabled": os.getenv("AUTONOMOUS_LOOP_ENABLED", "true").lower() == "true",
                "cycle_interval": int(os.getenv("CYCLE_INTERVAL", "300")),  # 5 minutes
                "max_concurrent_tasks": int(os.getenv("MAX_CONCURRENT_TASKS", "10")),
                "learning_enabled": os.getenv("LEARNING_ENABLED", "true").lower() == "true",
                "proactive_mode": os.getenv("PROACTIVE_MODE", "true").lower() == "true",
                "decision_threshold": float(os.getenv("DECISION_THRESHOLD", "0.7"))
            },

            # Audit logging
            "audit": {
                "enabled": os.getenv("AUDIT_ENABLED", "true").lower() == "true",
                "log_path": os.getenv("AUDIT_LOG_PATH", "AI_Employee_Vault/logs/audit.log"),
                "retention_days": int(os.getenv("AUDIT_RETENTION_DAYS", "90"))
            },

            # Error handling
            "error_handling": {
                "max_retries": int(os.getenv("MAX_RETRIES", "3")),
                "base_delay": float(os.getenv("RETRY_DELAY", "1.0")),
                "escalation_enabled": os.getenv("ESCALATION_ENABLED", "true").lower() == "true"
            },

            # Reporting
            "reporting": {
                "weekly_briefing_enabled": os.getenv("WEEKLY_BRIEFING_ENABLED", "true").lower() == "true",
                "briefing_output_path": os.getenv("BRIEFING_OUTPUT_PATH", "AI_Employee_Vault/reports"),
                "briefing_day": os.getenv("BRIEFING_DAY", "monday")
            }
        }

        # Load additional config from file if provided
        if self.config_path and self.config_path.exists():
            try:
                with open(self.config_path, 'r') as f:
                    file_config = json.load(f)
                    config.update(file_config)
                    self.logger.info(f"Loaded additional config from {self.config_path}")
            except Exception as e:
                self.logger.warning(f"Failed to load config file: {str(e)}")

        return config

    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value by key."""
        keys = key.split(".")
        value = self.config

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value

    def set(self, key: str, value: Any):
        """Set a configuration value."""
        keys = key.split(".")
        config = self.config

        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]

        config[keys[-1]] = value
        self.logger.debug(f"Set config {key} = {value}")

    def get_all(self) -> Dict[str, Any]:
        """Get all configuration values."""
        return self.config.copy()

    def save(self, path: str = None):
        """Save configuration to file."""
        path = Path(path) if path else self.config_path

        if not path:
            raise ValueError("No config path specified")

        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, 'w') as f:
            json.dump(self.config, f, indent=2)

        self.logger.info(f"Configuration saved to {path}")

    def validate(self) -> Dict[str, Any]:
        """Validate configuration."""
        errors = []
        warnings = []

        # Check required settings
        vault_path = Path(self.get("vault_path"))
        if not vault_path.exists():
            warnings.append(f"Vault path does not exist: {vault_path}")

        # Check MCP server ports
        mcp_servers = self.get("mcp_servers", {})
        for server_name, server_config in mcp_servers.items():
            port = server_config.get("port")
            if port and (port < 1024 or port > 65535):
                errors.append(f"Invalid port for {server_name} MCP server: {port}")

        # Check autonomous loop settings
        cycle_interval = self.get("autonomous_loop.cycle_interval")
        if cycle_interval and cycle_interval < 60:
            warnings.append(f"Cycle interval is very low: {cycle_interval}s (minimum recommended: 60s)")

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings
        }


# Global configuration instance
_config: Optional[Config] = None


def get_config(config_path: str = None) -> Config:
    """Get the global configuration instance."""
    global _config

    if _config is None:
        _config = Config(config_path)

    return _config


def reload_config(config_path: str = None) -> Config:
    """Reload the global configuration."""
    global _config
    _config = Config(config_path)
    return _config
