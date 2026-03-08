"""Command-line interface for the multi-agent system."""

import argparse
import json
import sys
from pathlib import Path
from agent_runner import AgentRunner


class AgentCLI:
    """CLI interface for interacting with the agent system."""

    def __init__(self):
        self.runner = None
        self.config_path = None

    def load_config(self, config_path: str = None):
        """Load configuration from file."""
        if config_path and Path(config_path).exists():
            with open(config_path, 'r') as f:
                config = json.load(f)
            self.runner = AgentRunner(config)
            print(f"✓ Configuration loaded from {config_path}")
        else:
            self.runner = AgentRunner()
            print("✓ Using default configuration")

    def run_task(self, args):
        """Run a single task."""
        task = {
            "agent_type": args.agent,
            "type": args.type,
            "description": args.description
        }

        # Add additional parameters from JSON if provided
        if args.params:
            try:
                params = json.loads(args.params)
                task.update(params)
            except json.JSONDecodeError:
                print("✗ Error: Invalid JSON in --params")
                return

        result = self.runner.run_task(task)
        print(f"\n✓ Task completed: {result.get('message', 'No message')}")
        if args.verbose:
            print(f"Full result: {json.dumps(result, indent=2)}")

    def run_batch(self, args):
        """Run multiple tasks from a file."""
        if not Path(args.file).exists():
            print(f"✗ Error: File not found: {args.file}")
            return

        with open(args.file, 'r') as f:
            tasks = json.load(f)

        print(f"Running {len(tasks)} tasks...")
        results = self.runner.run_batch(tasks)

        print(f"\n✓ Completed {len(results)} tasks")
        for i, result in enumerate(results):
            print(f"  Task {i+1}: {result.get('message', 'No message')}")

        if args.output:
            with open(args.output, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"\n✓ Results saved to {args.output}")

    def status(self, args):
        """Show status of all agents."""
        statuses = self.runner.get_all_statuses()
        print("\nAgent Statuses:")
        print("-" * 40)
        for agent, status in statuses.items():
            print(f"  {agent.capitalize():20} {status}")

    def delegate(self, args):
        """Delegate a task from CEO to another agent."""
        task = {
            "type": args.type,
            "description": args.description
        }

        if args.params:
            try:
                params = json.loads(args.params)
                task.update(params)
            except json.JSONDecodeError:
                print("✗ Error: Invalid JSON in --params")
                return

        result = self.runner.delegate_from_ceo(task, args.target)
        print(f"\n✓ Delegation completed: {result.get('message', 'No message')}")

    def interactive(self, args):
        """Start interactive mode."""
        print("\n" + "=" * 60)
        print("Multi-Agent System - Interactive Mode")
        print("=" * 60)
        print("\nAvailable agents: personal, business, social, autonomous, ceo")
        print("Type 'help' for commands, 'exit' to quit\n")

        while True:
            try:
                command = input("agent> ").strip()

                if not command:
                    continue

                if command == "exit":
                    print("Goodbye!")
                    break

                if command == "help":
                    self._show_help()
                    continue

                if command == "status":
                    self.status(args)
                    continue

                # Parse simple task command: agent_type task_type description
                parts = command.split(maxsplit=2)
                if len(parts) < 3:
                    print("✗ Invalid command. Format: <agent> <type> <description>")
                    continue

                agent_type, task_type, description = parts
                task = {
                    "agent_type": agent_type,
                    "type": task_type,
                    "description": description
                }

                result = self.runner.run_task(task)
                print(f"✓ {result.get('message', 'Task completed')}")

            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"✗ Error: {str(e)}")

    def _show_help(self):
        """Show help message in interactive mode."""
        print("\nCommands:")
        print("  <agent> <type> <description>  - Run a task")
        print("  status                         - Show agent statuses")
        print("  help                           - Show this help")
        print("  exit                           - Exit interactive mode")
        print("\nExample:")
        print("  personal schedule Schedule team meeting")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Multi-Agent System CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        "--config",
        help="Path to configuration file",
        default=None
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Run task command
    run_parser = subparsers.add_parser("run", help="Run a single task")
    run_parser.add_argument("agent", help="Agent type (personal, business, social, ceo, autonomous)")
    run_parser.add_argument("type", help="Task type")
    run_parser.add_argument("description", help="Task description")
    run_parser.add_argument("--params", help="Additional parameters as JSON")
    run_parser.add_argument("--verbose", action="store_true", help="Show full result")

    # Batch command
    batch_parser = subparsers.add_parser("batch", help="Run tasks from file")
    batch_parser.add_argument("file", help="Path to tasks JSON file")
    batch_parser.add_argument("--output", help="Save results to file")

    # Status command
    subparsers.add_parser("status", help="Show agent statuses")

    # Delegate command
    delegate_parser = subparsers.add_parser("delegate", help="Delegate task from CEO")
    delegate_parser.add_argument("target", help="Target agent name")
    delegate_parser.add_argument("type", help="Task type")
    delegate_parser.add_argument("description", help="Task description")
    delegate_parser.add_argument("--params", help="Additional parameters as JSON")

    # Interactive command
    subparsers.add_parser("interactive", help="Start interactive mode")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    cli = AgentCLI()
    cli.load_config(args.config)

    # Route to appropriate handler
    if args.command == "run":
        cli.run_task(args)
    elif args.command == "batch":
        cli.run_batch(args)
    elif args.command == "status":
        cli.status(args)
    elif args.command == "delegate":
        cli.delegate(args)
    elif args.command == "interactive":
        cli.interactive(args)


if __name__ == "__main__":
    main()
