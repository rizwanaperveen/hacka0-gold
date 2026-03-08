"""Example usage scenarios for the multi-agent system."""

from agent_runner import AgentRunner


def example_personal_tasks():
    """Example: Using the personal agent for daily tasks."""
    print("\n=== Personal Agent Example ===")

    runner = AgentRunner()

    tasks = [
        {
            "agent_type": "personal",
            "type": "schedule",
            "event": {"title": "Doctor Appointment", "time": "2:00 PM", "date": "2026-03-05"},
            "description": "Schedule doctor appointment"
        },
        {
            "agent_type": "personal",
            "type": "reminder",
            "reminder": {"text": "Buy groceries", "time": "6:00 PM"},
            "description": "Set grocery reminder"
        },
        {
            "agent_type": "personal",
            "type": "communication",
            "message": "Meeting confirmed for tomorrow",
            "recipient": "John Doe",
            "description": "Send confirmation message"
        }
    ]

    results = runner.run_batch(tasks)
    for result in results:
        print(f"✓ {result['message']}")


def example_business_operations():
    """Example: Using the business agent for operations."""
    print("\n=== Business Agent Example ===")

    runner = AgentRunner()

    tasks = [
        {
            "agent_type": "business",
            "type": "project",
            "project": {"name": "Q1 Marketing Campaign", "status": "in_progress", "budget": 10000},
            "description": "Track marketing project"
        },
        {
            "agent_type": "business",
            "type": "analytics",
            "metric": "customer_acquisition_cost",
            "value": 45.50,
            "description": "Update CAC metric"
        },
        {
            "agent_type": "business",
            "type": "report",
            "report_type": "monthly_revenue",
            "description": "Generate monthly report"
        }
    ]

    results = runner.run_batch(tasks)
    for result in results:
        print(f"✓ {result['message']}")


def example_social_media():
    """Example: Using the social agent for social media management."""
    print("\n=== Social Agent Example ===")

    runner = AgentRunner()

    tasks = [
        {
            "agent_type": "social",
            "type": "post",
            "content": "Check out our new product features! 🚀",
            "platform": "twitter",
            "description": "Post product update"
        },
        {
            "agent_type": "social",
            "type": "engage",
            "engagement_type": "comment",
            "target": "@customer_feedback",
            "description": "Respond to customer"
        },
        {
            "agent_type": "social",
            "type": "monitor",
            "keywords": ["brand_name", "product_name", "competitor"],
            "description": "Monitor brand mentions"
        }
    ]

    results = runner.run_batch(tasks)
    for result in results:
        print(f"✓ {result['message']}")


def example_ceo_coordination():
    """Example: Using the CEO agent to coordinate multiple agents."""
    print("\n=== CEO Agent Coordination Example ===")

    runner = AgentRunner()

    # CEO delegates tasks to different agents
    print("CEO delegating tasks...")

    runner.delegate_from_ceo(
        task={
            "type": "schedule",
            "event": {"title": "Board Meeting", "time": "9:00 AM"},
            "description": "Schedule board meeting"
        },
        target_agent="Personal Agent"
    )

    runner.delegate_from_ceo(
        task={
            "type": "analytics",
            "metric": "quarterly_revenue",
            "value": 250000,
            "description": "Update quarterly revenue"
        },
        target_agent="Business Agent"
    )

    runner.delegate_from_ceo(
        task={
            "type": "post",
            "content": "Quarterly results are in!",
            "platform": "linkedin",
            "description": "Announce quarterly results"
        },
        target_agent="Social Agent"
    )

    # Review all agent statuses
    review_task = {
        "agent_type": "ceo",
        "type": "review",
        "description": "Review all agent performance"
    }

    result = runner.run_task(review_task)
    print(f"\nCEO Review: {result['message']}")
    print("Agent Statuses:", result.get('results', []))


def example_autonomous_agent():
    """Example: Using the autonomous agent with goals."""
    print("\n=== Autonomous Agent Example ===")

    runner = AgentRunner()
    autonomous = runner.agents["autonomous"]

    # Set goals for the autonomous agent
    autonomous.set_goal({
        "description": "Optimize system performance",
        "priority": "high",
        "completed": False
    })

    autonomous.set_goal({
        "description": "Learn from user interactions",
        "priority": "medium",
        "completed": False
    })

    # Add tasks
    tasks = [
        {
            "agent_type": "autonomous",
            "type": "explore",
            "area": "system_metrics",
            "description": "Explore system metrics"
        },
        {
            "agent_type": "autonomous",
            "type": "learn",
            "data": {"user_behavior": "clicks", "frequency": 150},
            "description": "Learn from user data"
        },
        {
            "agent_type": "autonomous",
            "type": "optimize",
            "target": "response_time",
            "description": "Optimize response time"
        }
    ]

    results = runner.run_batch(tasks)
    for result in results:
        print(f"✓ {result['message']}")


def run_all_examples():
    """Run all example scenarios."""
    print("=" * 60)
    print("Multi-Agent System Examples")
    print("=" * 60)

    example_personal_tasks()
    example_business_operations()
    example_social_media()
    example_ceo_coordination()
    example_autonomous_agent()

    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    run_all_examples()
