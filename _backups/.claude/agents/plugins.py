"""Plugin system for extending agent functionality."""

import importlib
import inspect
from pathlib import Path
from typing import Dict, Any, List, Optional
import logging


class Plugin:
    """Base class for plugins."""

    def __init__(self, name: str):
        self.name = name
        self.enabled = True
        self.logger = logging.getLogger(f"Plugin.{name}")

    def initialize(self, config: Dict[str, Any]) -> None:
        """Initialize the plugin with configuration."""
        pass

    def on_task_start(self, task: Dict[str, Any]) -> None:
        """Called when a task starts."""
        pass

    def on_task_complete(self, task: Dict[str, Any], result: Dict[str, Any]) -> None:
        """Called when a task completes."""
        pass

    def on_agent_status_change(self, agent_name: str, old_status: str, new_status: str) -> None:
        """Called when an agent's status changes."""
        pass

    def shutdown(self) -> None:
        """Cleanup when plugin is disabled."""
        pass


class PluginManager:
    """Manage plugins for the agent system."""

    def __init__(self):
        self.plugins: Dict[str, Plugin] = {}
        self.plugin_dir = Path("plugins")
        self.logger = logging.getLogger("PluginManager")

    def load_plugin(self, plugin_path: str, config: Dict[str, Any] = None) -> bool:
        """Load a plugin from a file."""
        try:
            # Import the plugin module
            spec = importlib.util.spec_from_file_location("plugin", plugin_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Find Plugin subclasses
            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj) and issubclass(obj, Plugin) and obj != Plugin:
                    plugin_instance = obj(name)
                    plugin_instance.initialize(config or {})

                    self.plugins[name] = plugin_instance
                    self.logger.info(f"Plugin loaded: {name}")
                    return True

            self.logger.warning(f"No plugin class found in {plugin_path}")
            return False

        except Exception as e:
            self.logger.error(f"Failed to load plugin {plugin_path}: {str(e)}")
            return False

    def load_plugins_from_directory(self, directory: str = None) -> int:
        """Load all plugins from a directory."""
        plugin_dir = Path(directory) if directory else self.plugin_dir

        if not plugin_dir.exists():
            self.logger.warning(f"Plugin directory not found: {plugin_dir}")
            return 0

        loaded = 0
        for plugin_file in plugin_dir.glob("*.py"):
            if plugin_file.name.startswith("_"):
                continue

            if self.load_plugin(str(plugin_file)):
                loaded += 1

        self.logger.info(f"Loaded {loaded} plugins from {plugin_dir}")
        return loaded

    def enable_plugin(self, name: str) -> bool:
        """Enable a plugin."""
        if name in self.plugins:
            self.plugins[name].enabled = True
            self.logger.info(f"Plugin enabled: {name}")
            return True
        return False

    def disable_plugin(self, name: str) -> bool:
        """Disable a plugin."""
        if name in self.plugins:
            self.plugins[name].enabled = False
            self.plugins[name].shutdown()
            self.logger.info(f"Plugin disabled: {name}")
            return True
        return False

    def get_plugin(self, name: str) -> Optional[Plugin]:
        """Get a plugin by name."""
        return self.plugins.get(name)

    def list_plugins(self) -> List[Dict[str, Any]]:
        """List all loaded plugins."""
        return [
            {
                "name": name,
                "enabled": plugin.enabled,
                "class": plugin.__class__.__name__
            }
            for name, plugin in self.plugins.items()
        ]

    def trigger_task_start(self, task: Dict[str, Any]) -> None:
        """Trigger task start event for all plugins."""
        for plugin in self.plugins.values():
            if plugin.enabled:
                try:
                    plugin.on_task_start(task)
                except Exception as e:
                    self.logger.error(f"Plugin {plugin.name} error on task start: {str(e)}")

    def trigger_task_complete(self, task: Dict[str, Any], result: Dict[str, Any]) -> None:
        """Trigger task complete event for all plugins."""
        for plugin in self.plugins.values():
            if plugin.enabled:
                try:
                    plugin.on_task_complete(task, result)
                except Exception as e:
                    self.logger.error(f"Plugin {plugin.name} error on task complete: {str(e)}")

    def trigger_status_change(self, agent_name: str, old_status: str, new_status: str) -> None:
        """Trigger status change event for all plugins."""
        for plugin in self.plugins.values():
            if plugin.enabled:
                try:
                    plugin.on_agent_status_change(agent_name, old_status, new_status)
                except Exception as e:
                    self.logger.error(f"Plugin {plugin.name} error on status change: {str(e)}")

    def shutdown_all(self) -> None:
        """Shutdown all plugins."""
        for plugin in self.plugins.values():
            try:
                plugin.shutdown()
            except Exception as e:
                self.logger.error(f"Error shutting down plugin {plugin.name}: {str(e)}")


# Example plugin
class LoggingPlugin(Plugin):
    """Example plugin that logs all events."""

    def __init__(self, name: str):
        super().__init__(name)
        self.task_count = 0

    def initialize(self, config: Dict[str, Any]) -> None:
        """Initialize the plugin."""
        self.logger.info("Logging plugin initialized")

    def on_task_start(self, task: Dict[str, Any]) -> None:
        """Log task start."""
        self.task_count += 1
        self.logger.info(f"Task started: {task.get('description')} (Total: {self.task_count})")

    def on_task_complete(self, task: Dict[str, Any], result: Dict[str, Any]) -> None:
        """Log task completion."""
        status = result.get("status", "unknown")
        self.logger.info(f"Task completed: {task.get('description')} - Status: {status}")

    def on_agent_status_change(self, agent_name: str, old_status: str, new_status: str) -> None:
        """Log status change."""
        self.logger.info(f"Agent {agent_name}: {old_status} -> {new_status}")

    def shutdown(self) -> None:
        """Cleanup."""
        self.logger.info(f"Logging plugin shutdown. Total tasks processed: {self.task_count}")


def example_usage():
    """Example usage of the plugin system."""
    manager = PluginManager()

    # Load plugins from directory
    manager.load_plugins_from_directory()

    # Or load a specific plugin
    # manager.load_plugin("plugins/my_plugin.py")

    # List plugins
    plugins = manager.list_plugins()
    print("Loaded plugins:", plugins)

    # Trigger events
    task = {"agent_type": "personal", "description": "Test task"}
    manager.trigger_task_start(task)

    result = {"status": "completed", "message": "Done"}
    manager.trigger_task_complete(task, result)

    # Shutdown
    manager.shutdown_all()


if __name__ == "__main__":
    example_usage()
