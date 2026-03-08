"""Setup script for the multi-agent system."""

import os
import sys
import json
from pathlib import Path


def create_directories():
    """Create necessary directories."""
    directories = ["data", "logs"]

    for directory in directories:
        path = Path(directory)
        if not path.exists():
            path.mkdir(parents=True)
            print(f"✓ Created directory: {directory}")
        else:
            print(f"  Directory already exists: {directory}")


def create_config():
    """Create default configuration file."""
    config_path = Path("config.json")

    if config_path.exists():
        print("  Configuration file already exists: config.json")
        return

    default_config = {
        "log_level": "INFO",
        "ceo": {
            "max_agents": 10,
            "coordination_mode": "hierarchical"
        },
        "personal": {
            "calendar_sync": True,
            "reminder_interval": 300,
            "notification_enabled": True
        },
        "business": {
            "analytics_enabled": True,
            "report_frequency": "daily",
            "project_tracking": True
        },
        "social": {
            "platforms": ["twitter", "linkedin", "facebook"],
            "auto_post": False,
            "engagement_threshold": 100
        },
        "autonomous": {
            "learning_enabled": True,
            "exploration_mode": "balanced",
            "goal_priority": "medium",
            "max_autonomous_actions": 50
        }
    }

    with open(config_path, 'w') as f:
        json.dump(default_config, f, indent=2)

    print(f"✓ Created configuration file: config.json")


def create_env_file():
    """Create .env file from example."""
    env_path = Path(".env")
    env_example_path = Path(".env.example")

    if env_path.exists():
        print("  Environment file already exists: .env")
        return

    if env_example_path.exists():
        with open(env_example_path, 'r') as f:
            content = f.read()

        with open(env_path, 'w') as f:
            f.write(content)

        print(f"✓ Created environment file: .env")
    else:
        print("  Warning: .env.example not found")


def check_dependencies():
    """Check if required dependencies are installed."""
    print("\nChecking dependencies...")

    dependencies = {
        "flask": "Flask (for API server)",
        "flask_cors": "Flask-CORS (for API server)"
    }

    missing = []

    for module, description in dependencies.items():
        try:
            __import__(module)
            print(f"✓ {description}")
        except ImportError:
            print(f"✗ {description} - NOT INSTALLED")
            missing.append(module)

    if missing:
        print("\nTo install missing dependencies, run:")
        print("  pip install -r requirements.txt")
        return False

    return True


def run_tests():
    """Run basic tests to verify installation."""
    print("\nRunning basic tests...")

    try:
        from agent_runner import AgentRunner

        runner = AgentRunner()
        print("✓ AgentRunner initialized successfully")

        # Test a simple task
        task = {
            "agent_type": "personal",
            "type": "schedule",
            "event": {"title": "Test", "time": "10:00 AM"},
            "description": "Test task"
        }

        result = runner.run_task(task)

        if result.get("status") == "completed":
            print("✓ Test task completed successfully")
            return True
        else:
            print("✗ Test task failed")
            return False

    except Exception as e:
        print(f"✗ Test failed: {str(e)}")
        return False


def main():
    """Main setup function."""
    print("=" * 60)
    print("Multi-Agent System Setup")
    print("=" * 60)
    print()

    # Create directories
    print("Creating directories...")
    create_directories()
    print()

    # Create configuration
    print("Setting up configuration...")
    create_config()
    create_env_file()
    print()

    # Check dependencies
    deps_ok = check_dependencies()
    print()

    # Run tests
    if deps_ok:
        tests_ok = run_tests()
        print()
    else:
        tests_ok = False
        print("\nSkipping tests due to missing dependencies")
        print()

    # Summary
    print("=" * 60)
    print("Setup Summary")
    print("=" * 60)

    if deps_ok and tests_ok:
        print("\n✓ Setup completed successfully!")
        print("\nNext steps:")
        print("  1. Review config.json and adjust settings")
        print("  2. Run examples: python examples.py")
        print("  3. Start CLI: python cli.py interactive")
        print("  4. Start API: python api_server.py")
        print("  5. Open dashboard.html in your browser")
    else:
        print("\n⚠ Setup completed with warnings")
        print("\nPlease install missing dependencies:")
        print("  pip install -r requirements.txt")
        print("\nThen run setup again:")
        print("  python setup.py")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
