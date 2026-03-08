#!/usr/bin/env python3
"""
Quick Start Script - Get the multi-agent system running in seconds
"""

import os
import sys
from pathlib import Path


def print_banner():
    """Print welcome banner."""
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║     Multi-Agent System with Skills - Quick Start         ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """)


def check_structure():
    """Check if the project structure exists."""
    print("Checking project structure...")

    required_dirs = [
        "agents",
        "skills"
    ]

    required_files = [
        "agents/agent_runner.py",
        "agents/main.py",
        "skills/gmail_skill.py",
        "README.md"
    ]

    all_good = True

    for directory in required_dirs:
        if Path(directory).exists():
            print(f"  ✓ {directory}/ directory found")
        else:
            print(f"  ✗ {directory}/ directory missing")
            all_good = False

    for file in required_files:
        if Path(file).exists():
            print(f"  ✓ {file} found")
        else:
            print(f"  ✗ {file} missing")
            all_good = False

    return all_good


def show_menu():
    """Show interactive menu."""
    print("\n" + "=" * 60)
    print("What would you like to do?")
    print("=" * 60)
    print()
    print("1. Run agent examples")
    print("2. Start API server")
    print("3. Start CLI interactive mode")
    print("4. Run tests")
    print("5. Run diagnostics")
    print("6. Show system status")
    print("7. View documentation")
    print("8. Exit")
    print()


def run_examples():
    """Run example scenarios."""
    print("\nRunning examples...")
    os.chdir("agents")
    os.system("python examples.py")
    os.chdir("..")


def start_api():
    """Start API server."""
    print("\nStarting API server...")
    print("Access at: http://localhost:5000")
    print("Dashboard: Open agents/dashboard.html in your browser")
    print()
    os.chdir("agents")
    os.system("python api_server.py")
    os.chdir("..")


def start_cli():
    """Start CLI interactive mode."""
    print("\nStarting CLI interactive mode...")
    os.chdir("agents")
    os.system("python cli.py interactive")
    os.chdir("..")


def run_tests():
    """Run test suite."""
    print("\nRunning tests...")
    os.chdir("agents")
    os.system("python test_agents.py")
    os.chdir("..")


def run_diagnostics():
    """Run system diagnostics."""
    print("\nRunning diagnostics...")
    os.chdir("agents")
    os.system("python diagnostics.py")
    os.chdir("..")


def show_status():
    """Show system status."""
    print("\nSystem Status:")
    os.chdir("agents")
    os.system("python main.py status")
    os.chdir("..")


def view_docs():
    """View documentation."""
    print("\n" + "=" * 60)
    print("Documentation Files:")
    print("=" * 60)
    print()
    print("Main Documentation:")
    print("  - README.md - Complete project overview")
    print("  - agents/README.md - Agent system documentation")
    print("  - skills/README.md - Skills library documentation")
    print()
    print("Getting Started:")
    print("  - agents/QUICKSTART.md - 5-minute quick start")
    print("  - agents/INTEGRATION.md - API integration guide")
    print()
    print("Reference:")
    print("  - agents/PROJECT_STRUCTURE.md - Architecture overview")
    print("  - agents/CHANGELOG.md - Version history")
    print()
    print("Examples:")
    print("  - agents/examples.py - Usage examples")
    print("  - agents/tasks.example.json - Example tasks")
    print()


def main():
    """Main entry point."""
    print_banner()

    # Check structure
    if not check_structure():
        print("\n⚠ Warning: Some files are missing!")
        print("Please ensure you're in the .claude directory")
        print()
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            sys.exit(1)

    # Main loop
    while True:
        show_menu()

        try:
            choice = input("Enter your choice (1-8): ").strip()

            if choice == "1":
                run_examples()
            elif choice == "2":
                start_api()
            elif choice == "3":
                start_cli()
            elif choice == "4":
                run_tests()
            elif choice == "5":
                run_diagnostics()
            elif choice == "6":
                show_status()
            elif choice == "7":
                view_docs()
            elif choice == "8":
                print("\nGoodbye!")
                break
            else:
                print("\n✗ Invalid choice. Please enter 1-8.")

            if choice in ["1", "4", "5", "6"]:
                input("\nPress Enter to continue...")

        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\n✗ Error: {str(e)}")
            input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
