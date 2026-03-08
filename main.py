"""
Main Entry Point - Gold Tier Autonomous AI Employee

This is the single entry point for running the entire AI employee system.

Usage:
    python main.py                      # Run with default configuration
    python main.py --config config.json # Run with custom configuration
    python main.py --mode autonomous    # Run in autonomous mode
    python main.py --mode server        # Run MCP servers only
    python main.py --mode cli           # Run in CLI interactive mode
"""

import argparse
import asyncio
import logging
import sys
from datetime import datetime
from pathlib import Path

from config import get_config, Config
from core.orchestrator import CoreOrchestrator
from core.autonomous_loop.ralph_wiggum import RalphWiggumLoop
from core.audit.audit_logger import AuditLogger


def setup_logging(config: Config):
    """Setup logging configuration."""
    log_level = getattr(logging, config.get("log_level", "INFO").upper())
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    logging.basicConfig(
        level=log_level,
        format=log_format,
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("AI_Employee_Vault/logs/system.log")
        ]
    )

    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("fastapi").setLevel(logging.WARNING)


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Gold Tier Autonomous AI Employee"
    )

    parser.add_argument(
        "--config",
        type=str,
        default=None,
        help="Path to configuration file"
    )

    parser.add_argument(
        "--mode",
        type=str,
        default="autonomous",
        choices=["autonomous", "server", "cli", "once"],
        help="Running mode"
    )

    parser.add_argument(
        "--task",
        type=str,
        default=None,
        help="Single task to execute (for --mode once)"
    )

    parser.add_argument(
        "--servers",
        nargs="+",
        default=["personal", "business", "social"],
        help="MCP servers to start (for --mode server)"
    )

    return parser.parse_args()


async def run_autonomous_mode(config: Config):
    """Run in autonomous mode with Ralph Wiggum loop."""
    logger = logging.getLogger("Main")
    logger.info("Starting autonomous mode...")

    # Initialize Ralph Wiggum loop
    loop = RalphWiggumLoop(config={
        "orchestrator": config.get_all(),
        "audit_log_path": config.get("audit.log_path"),
        "cycle_interval": config.get("autonomous_loop.cycle_interval"),
        "max_concurrent_tasks": config.get("autonomous_loop.max_concurrent_tasks"),
        "learning_enabled": config.get("autonomous_loop.learning_enabled"),
        "proactive_mode": config.get("autonomous_loop.proactive_mode"),
        "decision_threshold": config.get("autonomous_loop.decision_threshold"),
        "observation_sources": [
            "gmail",
            "calendar",
            "tasks",
            "social_media",
            "business_metrics"
        ]
    })

    try:
        await loop.start()
    except KeyboardInterrupt:
        logger.info("Shutdown requested...")
        await loop.stop()
    except Exception as e:
        logger.error(f"Autonomous loop error: {str(e)}")
        raise


async def run_server_mode(config: Config, servers: list):
    """Run MCP servers only."""
    logger = logging.getLogger("Main")
    logger.info(f"Starting server mode with servers: {servers}")

    import uvicorn
    from multiprocessing import Process

    processes = []

    for server_name in servers:
        if server_name == "personal":
            port = config.get("mcp_servers.personal.port", 8001)
        elif server_name == "business":
            port = config.get("mcp_servers.business.port", 8002)
        elif server_name == "social":
            port = config.get("mcp_servers.social.port", 8003)
        else:
            logger.warning(f"Unknown server: {server_name}")
            continue

        logger.info(f"Starting {server_name} MCP server on port {port}")

        process = Process(
            target=uvicorn.run,
            kwargs={
                "app": f"mcp_servers.{server_name}_server.server:app",
                "host": "0.0.0.0",
                "port": port,
                "log_level": "warning"
            }
        )
        process.start()
        processes.append(process)

    try:
        # Keep running
        for process in processes:
            process.join()
    except KeyboardInterrupt:
        logger.info("Shutdown requested...")
        for process in processes:
            process.terminate()


async def run_cli_mode(config: Config):
    """Run in CLI interactive mode."""
    logger = logging.getLogger("Main")
    logger.info("Starting CLI mode...")

    # Initialize orchestrator
    orchestrator = CoreOrchestrator(config=config.get_all())

    try:
        await orchestrator.initialize()

        print("\n=== AI Employee CLI Mode ===")
        print("Enter commands (type 'quit' to exit):")
        print("  - task <description>  : Execute a task")
        print("  - status              : Show system status")
        print("  - briefing            : Generate weekly briefing")
        print()

        while True:
            try:
                command = input("> ").strip()

                if command.lower() == "quit":
                    break
                elif command.lower() == "status":
                    status = orchestrator.get_status()
                    print(f"\nSystem Status: {status}\n")
                elif command.lower() == "briefing":
                    from core.reporting.weekly_briefing import WeeklyBriefingGenerator
                    generator = WeeklyBriefingGenerator()
                    result = await generator.generate_briefing()
                    print(f"\nBriefing generated: {result.get('briefing_file')}\n")
                elif command.startswith("task "):
                    task_desc = command[5:].strip()
                    task = {
                        "id": f"cli_{datetime.now().timestamp()}",
                        "type": "manual",
                        "domain": "personal",
                        "description": task_desc
                    }
                    result = await orchestrator.execute_task(task)
                    print(f"\nTask result: {result}\n")
                else:
                    print("Unknown command. Available commands: task, status, briefing, quit\n")

            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Error: {str(e)}\n")

    finally:
        await orchestrator.shutdown()


async def run_once_mode(config: Config, task_desc: str):
    """Run a single task and exit."""
    logger = logging.getLogger("Main")
    logger.info(f"Executing single task: {task_desc}")

    # Initialize orchestrator
    orchestrator = CoreOrchestrator(config=config.get_all())

    try:
        await orchestrator.initialize()

        task = {
            "id": f"once_{datetime.now().timestamp()}",
            "type": "manual",
            "domain": "personal",
            "description": task_desc
        }

        result = await orchestrator.execute_task(task)
        print(f"Task result: {result}")

    finally:
        await orchestrator.shutdown()


async def main():
    """Main entry point."""
    args = parse_args()

    # Load configuration
    config = get_config(args.config)

    # Setup logging
    setup_logging(config)

    logger = logging.getLogger("Main")
    logger.info("=" * 60)
    logger.info("Gold Tier Autonomous AI Employee")
    logger.info(f"Environment: {config.get('environment')}")
    logger.info(f"Mode: {args.mode}")
    logger.info("=" * 60)

    # Validate configuration
    validation = config.validate()
    if validation["errors"]:
        for error in validation["errors"]:
            logger.error(f"Configuration error: {error}")
        sys.exit(1)

    if validation["warnings"]:
        for warning in validation["warnings"]:
            logger.warning(f"Configuration warning: {warning}")

    # Ensure vault directories exist
    vault_path = Path(config.get("vault_path"))
    for subdir in ["Inbox", "Needs_Action", "Pending_Approval", "Approved",
                   "Plans", "Done", "Rejected", "logs", "reports", "data", "config"]:
        (vault_path / subdir).mkdir(parents=True, exist_ok=True)

    # Run based on mode
    if args.mode == "autonomous":
        await run_autonomous_mode(config)
    elif args.mode == "server":
        await run_server_mode(config, args.servers)
    elif args.mode == "cli":
        await run_cli_mode(config)
    elif args.mode == "once":
        if not args.task:
            logger.error("--task is required for --mode once")
            sys.exit(1)
        await run_once_mode(config, args.task)
    else:
        logger.error(f"Unknown mode: {args.mode}")
        sys.exit(1)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nShutdown complete")
    except Exception as e:
        logging.error(f"Fatal error: {str(e)}")
        sys.exit(1)
