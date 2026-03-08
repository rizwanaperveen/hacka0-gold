#!/usr/bin/env python3
"""
Gold Tier Setup Script

Initializes the Gold Tier AI Employee system:
- Creates necessary directories
- Initializes database
- Validates configuration
- Sets up integrations
"""

import os
import sys
import logging
from pathlib import Path
import subprocess


def setup_logging():
    """Setup logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger("GoldTierSetup")


def create_directories(logger):
    """Create necessary directory structure."""
    logger.info("Creating directory structure...")

    directories = [
        "AI_Employee_Vault/logs",
        "AI_Employee_Vault/data",
        "AI_Employee_Vault/reports",
        "AI_Employee_Vault/config",
        "AI_Employee_Vault/Needs_Action",
        "AI_Employee_Vault/Plans",
        "AI_Employee_Vault/Pending_Approval",
        "AI_Employee_Vault/Approved",
        "AI_Employee_Vault/Done",
    ]

    for directory in directories:
        path = Path(directory)
        path.mkdir(parents=True, exist_ok=True)
        logger.info(f"  ✓ Created {directory}")


def check_python_version(logger):
    """Check Python version."""
    logger.info("Checking Python version...")

    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        logger.info(f"  ✓ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        logger.error(f"  ✗ Python {version.major}.{version.minor} (requires 3.8+)")
        return False


def install_dependencies(logger):
    """Install Python dependencies."""
    logger.info("Installing dependencies...")

    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        logger.info("  ✓ Dependencies installed")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"  ✗ Failed to install dependencies: {str(e)}")
        return False


def check_env_file(logger):
    """Check if .env file exists."""
    logger.info("Checking environment configuration...")

    env_file = Path(".env")
    env_example = Path(".env.example")

    if env_file.exists():
        logger.info("  ✓ .env file exists")
        return True
    elif env_example.exists():
        logger.warning("  ⚠ .env file not found")
        logger.info("  Creating .env from .env.example...")

        with open(env_example, 'r') as src:
            content = src.read()

        with open(env_file, 'w') as dst:
            dst.write(content)

        logger.info("  ✓ Created .env file")
        logger.warning("  ⚠ Please edit .env with your API keys")
        return True
    else:
        logger.error("  ✗ No .env.example file found")
        return False


def initialize_database(logger):
    """Initialize database."""
    logger.info("Initializing database...")

    db_path = Path("AI_Employee_Vault/data/employee.db")

    if db_path.exists():
        logger.info("  ✓ Database already exists")
        return True

    try:
        import sqlite3

        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()

        # Create basic tables
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_id TEXT UNIQUE,
                domain TEXT,
                type TEXT,
                description TEXT,
                status TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                entry_id TEXT UNIQUE,
                category TEXT,
                event_type TEXT,
                description TEXT,
                metadata TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()
        conn.close()

        logger.info("  ✓ Database initialized")
        return True

    except Exception as e:
        logger.error(f"  ✗ Failed to initialize database: {str(e)}")
        return False


def verify_installation(logger):
    """Verify installation."""
    logger.info("Verifying installation...")

    checks = []

    # Check core modules
    try:
        from core.orchestration.orchestrator import CoreOrchestrator
        checks.append(("Core orchestrator", True))
    except ImportError as e:
        checks.append(("Core orchestrator", False))

    try:
        from core.autonomous_loop.ralph_wiggum import RalphWiggumLoop
        checks.append(("Ralph Wiggum loop", True))
    except ImportError:
        checks.append(("Ralph Wiggum loop", False))

    try:
        from agents.coordinators.ceo_agent import CEOAgent
        checks.append(("CEO agent", True))
    except ImportError:
        checks.append(("CEO agent", False))

    try:
        from skills.personal.email_skill import EmailSkill
        checks.append(("Email skill", True))
    except ImportError:
        checks.append(("Email skill", False))

    # Print results
    all_passed = True
    for name, passed in checks:
        if passed:
            logger.info(f"  ✓ {name}")
        else:
            logger.error(f"  ✗ {name}")
            all_passed = False

    return all_passed


def main():
    """Main setup function."""
    logger = setup_logging()

    print("=" * 60)
    print("Gold Tier AI Employee - Setup")
    print("=" * 60)
    print()

    # Run setup steps
    steps = [
        ("Checking Python version", check_python_version),
        ("Creating directories", create_directories),
        ("Checking environment file", check_env_file),
        ("Installing dependencies", install_dependencies),
        ("Initializing database", initialize_database),
        ("Verifying installation", verify_installation),
    ]

    results = []
    for step_name, step_func in steps:
        try:
            result = step_func(logger)
            results.append((step_name, result))
        except Exception as e:
            logger.error(f"Error in {step_name}: {str(e)}")
            results.append((step_name, False))

    # Print summary
    print()
    print("=" * 60)
    print("Setup Summary")
    print("=" * 60)

    all_passed = all(result for _, result in results)

    for step_name, result in results:
        status = "✓" if result else "✗"
        print(f"{status} {step_name}")

    print()

    if all_passed:
        print("✓ Setup completed successfully!")
        print()
        print("Next steps:")
        print("  1. Edit .env with your API keys")
        print("  2. Run: python core/autonomous_loop/ralph_wiggum.py")
        print("  3. Or: python mcp_servers/personal_server/server.py")
        print()
        return 0
    else:
        print("✗ Setup completed with errors")
        print()
        print("Please fix the errors above and run setup again.")
        print()
        return 1


if __name__ == "__main__":
    sys.exit(main())
