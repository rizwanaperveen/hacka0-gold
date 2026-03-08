"""Main launcher script for the multi-agent system."""

import sys
import argparse
from pathlib import Path


def print_banner():
    """Print the application banner."""
    banner = """
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║           Multi-Agent System v1.0.0                       ║
    ║           Task Automation & Coordination                  ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """
    print(banner)


def launch_api_server(args):
    """Launch the API server."""
    print("Starting API server...")
    from api_server import main
    main()


def launch_cli(args):
    """Launch the CLI interface."""
    print("Starting CLI...")
    from cli import main
    sys.argv = ["cli.py"] + args.cli_args
    main()


def launch_interactive(args):
    """Launch interactive mode."""
    print("Starting interactive mode...")
    from cli import main
    sys.argv = ["cli.py", "interactive"]
    main()


def launch_scheduler(args):
    """Launch the task scheduler."""
    print("Starting task scheduler...")
    from scheduler import example_usage
    example_usage()


def run_examples(args):
    """Run example scenarios."""
    print("Running examples...")
    from examples import run_all_examples
    run_all_examples()


def run_tests(args):
    """Run the test suite."""
    print("Running tests...")
    from test_agents import run_tests
    run_tests()


def run_setup(args):
    """Run the setup script."""
    print("Running setup...")
    from setup import main
    main()


def show_status(args):
    """Show system status."""
    print("Checking system status...\n")

    try:
        from agent_runner import AgentRunner

        runner = AgentRunner()
        statuses = runner.get_all_statuses()

        print("Agent Statuses:")
        print("-" * 40)
        for agent, status in statuses.items():
            status_icon = "✓" if status == "idle" else "⚙"
            print(f"  {status_icon} {agent.capitalize():20} {status}")

        print("\n✓ System is operational")

    except Exception as e:
        print(f"✗ Error checking status: {str(e)}")
        sys.exit(1)


def show_info(args):
    """Show system information."""
    print("System Information:")
    print("-" * 60)

    # Python version
    print(f"Python Version: {sys.version.split()[0]}")

    # Check dependencies
    dependencies = {
        "flask": "Flask",
        "flask_cors": "Flask-CORS"
    }

    print("\nDependencies:")
    for module, name in dependencies.items():
        try:
            __import__(module)
            print(f"  ✓ {name}")
        except ImportError:
            print(f"  ✗ {name} (not installed)")

    # Check files
    print("\nConfiguration:")
    config_files = ["config.json", ".env", "agents.db"]
    for file in config_files:
        exists = Path(file).exists()
        icon = "✓" if exists else "✗"
        print(f"  {icon} {file}")

    print("\nAvailable Agents:")
    agents = ["CEO", "Personal", "Business", "Social", "Autonomous"]
    for agent in agents:
        print(f"  • {agent} Agent")

    print("\nDocumentation:")
    docs = ["README.md", "QUICKSTART.md", "INTEGRATION.md"]
    for doc in docs:
        print(f"  • {doc}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Multi-Agent System Launcher",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py api              Start the API server
  python main.py cli status       Run CLI status command
  python main.py interactive      Start interactive mode
  python main.py examples         Run example scenarios
  python main.py tests            Run test suite
  python main.py setup            Run setup wizard
  python main.py status           Show system status
  python main.py info             Show system information
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # API server
    subparsers.add_parser("api", help="Start the API server")

    # CLI
    cli_parser = subparsers.add_parser("cli", help="Run CLI commands")
    cli_parser.add_argument("cli_args", nargs="*", help="CLI arguments")

    # Interactive
    subparsers.add_parser("interactive", help="Start interactive mode")

    # Scheduler
    subparsers.add_parser("scheduler", help="Start task scheduler")

    # Examples
    subparsers.add_parser("examples", help="Run example scenarios")

    # Tests
    subparsers.add_parser("tests", help="Run test suite")

    # Setup
    subparsers.add_parser("setup", help="Run setup wizard")

    # Status
    subparsers.add_parser("status", help="Show system status")

    # Info
    subparsers.add_parser("info", help="Show system information")

    args = parser.parse_args()

    if not args.command:
        print_banner()
        parser.print_help()
        sys.exit(0)

    print_banner()

    # Route to appropriate handler
    commands = {
        "api": launch_api_server,
        "cli": launch_cli,
        "interactive": launch_interactive,
        "scheduler": launch_scheduler,
        "examples": run_examples,
        "tests": run_tests,
        "setup": run_setup,
        "status": show_status,
        "info": show_info
    }

    handler = commands.get(args.command)
    if handler:
        try:
            handler(args)
        except KeyboardInterrupt:
            print("\n\nShutdown requested. Goodbye!")
            sys.exit(0)
        except Exception as e:
            print(f"\n✗ Error: {str(e)}")
            sys.exit(1)
    else:
        print(f"Unknown command: {args.command}")
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
