"""Unit tests for the multi-agent system."""

import unittest
from agents.base_agent import BaseAgent
from agents.personal_agent import PersonalAgent
from agents.business_agent import BusinessAgent
from agents.social_agent import SocialAgent
from agents.ceo_agent import CEOAgent
from agents.autonomous_agent import AutonomousAgent


class TestBaseAgent(unittest.TestCase):
    """Test cases for BaseAgent."""

    def setUp(self):
        """Set up test fixtures."""
        class TestAgent(BaseAgent):
            def process_task(self, task):
                return {"status": "completed", "message": "Test task completed"}

        self.agent = TestAgent("Test Agent")

    def test_initialization(self):
        """Test agent initialization."""
        self.assertEqual(self.agent.name, "Test Agent")
        self.assertEqual(self.agent.status, "idle")
        self.assertEqual(len(self.agent.task_queue), 0)

    def test_add_task(self):
        """Test adding tasks to queue."""
        task = {"description": "Test task"}
        self.agent.add_task(task)
        self.assertEqual(len(self.agent.task_queue), 1)

    def test_status_change(self):
        """Test status changes."""
        self.agent.set_status("running")
        self.assertEqual(self.agent.get_status(), "running")


class TestPersonalAgent(unittest.TestCase):
    """Test cases for PersonalAgent."""

    def setUp(self):
        """Set up test fixtures."""
        self.agent = PersonalAgent()

    def test_schedule_task(self):
        """Test scheduling functionality."""
        task = {
            "type": "schedule",
            "event": {"title": "Meeting", "time": "10:00 AM"},
            "description": "Schedule meeting"
        }
        result = self.agent.process_task(task)
        self.assertEqual(result["status"], "completed")
        self.assertEqual(len(self.agent.calendar), 1)

    def test_reminder_task(self):
        """Test reminder functionality."""
        task = {
            "type": "reminder",
            "reminder": {"text": "Buy milk", "time": "5:00 PM"},
            "description": "Set reminder"
        }
        result = self.agent.process_task(task)
        self.assertEqual(result["status"], "completed")
        self.assertEqual(len(self.agent.reminders), 1)


class TestBusinessAgent(unittest.TestCase):
    """Test cases for BusinessAgent."""

    def setUp(self):
        """Set up test fixtures."""
        self.agent = BusinessAgent()

    def test_project_task(self):
        """Test project tracking."""
        task = {
            "type": "project",
            "project": {"name": "Project X", "status": "active"},
            "description": "Track project"
        }
        result = self.agent.process_task(task)
        self.assertEqual(result["status"], "completed")
        self.assertEqual(len(self.agent.projects), 1)

    def test_analytics_task(self):
        """Test analytics functionality."""
        task = {
            "type": "analytics",
            "metric": "revenue",
            "value": 10000,
            "description": "Update analytics"
        }
        result = self.agent.process_task(task)
        self.assertEqual(result["status"], "completed")
        self.assertIn("revenue", self.agent.analytics)


class TestSocialAgent(unittest.TestCase):
    """Test cases for SocialAgent."""

    def setUp(self):
        """Set up test fixtures."""
        self.agent = SocialAgent()

    def test_post_task(self):
        """Test posting functionality."""
        task = {
            "type": "post",
            "content": "Test post",
            "platform": "twitter",
            "description": "Post to social media"
        }
        result = self.agent.process_task(task)
        self.assertEqual(result["status"], "completed")
        self.assertEqual(len(self.agent.posts), 1)

    def test_engagement_task(self):
        """Test engagement functionality."""
        task = {
            "type": "engage",
            "engagement_type": "like",
            "target": "@user",
            "description": "Engage with content"
        }
        result = self.agent.process_task(task)
        self.assertEqual(result["status"], "completed")
        self.assertEqual(len(self.agent.engagements), 1)


class TestCEOAgent(unittest.TestCase):
    """Test cases for CEOAgent."""

    def setUp(self):
        """Set up test fixtures."""
        self.ceo = CEOAgent()
        self.personal = PersonalAgent()
        self.business = BusinessAgent()

    def test_register_agent(self):
        """Test agent registration."""
        self.ceo.register_agent(self.personal)
        self.assertEqual(len(self.ceo.agents), 1)

    def test_delegation(self):
        """Test task delegation."""
        self.ceo.register_agent(self.personal)
        task = {
            "type": "delegate",
            "agent": "Personal Agent",
            "subtask": {"type": "schedule", "event": {"title": "Meeting"}},
            "description": "Delegate scheduling"
        }
        result = self.ceo.process_task(task)
        self.assertEqual(result["status"], "completed")

    def test_find_agent(self):
        """Test finding agents by name."""
        self.ceo.register_agent(self.personal)
        agent = self.ceo._find_agent("Personal Agent")
        self.assertIsNotNone(agent)
        self.assertEqual(agent.name, "Personal Agent")


class TestAutonomousAgent(unittest.TestCase):
    """Test cases for AutonomousAgent."""

    def setUp(self):
        """Set up test fixtures."""
        self.agent = AutonomousAgent()

    def test_set_goal(self):
        """Test goal setting."""
        goal = {"description": "Test goal", "priority": "high"}
        self.agent.set_goal(goal)
        self.assertEqual(len(self.agent.goals), 1)

    def test_decide_action(self):
        """Test autonomous decision making."""
        goal = {"description": "Test goal", "priority": "high"}
        self.agent.set_goal(goal)
        action = self.agent.decide_action()
        self.assertIn("action", action)
        self.assertIn("goal", action)

    def test_learning_task(self):
        """Test learning functionality."""
        task = {
            "type": "learn",
            "data": {"key": "value"},
            "description": "Learn from data"
        }
        result = self.agent.process_task(task)
        self.assertEqual(result["status"], "completed")
        self.assertEqual(len(self.agent.learning_data), 1)


def run_tests():
    """Run all tests."""
    unittest.main(argv=[''], verbosity=2, exit=False)


if __name__ == "__main__":
    run_tests()
