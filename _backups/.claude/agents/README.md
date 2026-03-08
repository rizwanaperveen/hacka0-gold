# Multi-Agent System

A flexible multi-agent system for task automation and coordination.

## Architecture

The system consists of five specialized agents coordinated by a CEO agent:

### Agents

1. **CEO Agent** (`ceo_agent.py`)
   - High-level coordination and strategy
   - Delegates tasks to specialized agents
   - Reviews agent performance
   - Makes strategic decisions

2. **Personal Agent** (`personal_agent.py`)
   - Manages personal tasks and schedules
   - Handles reminders and calendar events
   - Manages personal communications

3. **Business Agent** (`business_agent.py`)
   - Handles business operations
   - Tracks projects and analytics
   - Generates reports
   - Supports business decisions

4. **Social Agent** (`social_agent.py`)
   - Manages social media presence
   - Handles engagement and networking
   - Monitors brand mentions
   - Posts content across platforms

5. **Autonomous Agent** (`autonomous_agent.py`)
   - Self-directed with independent goals
   - Learns from data and interactions
   - Explores and optimizes autonomously
   - Makes independent decisions

## Installation

```bash
# No external dependencies required for basic functionality
# The system uses only Python standard library

# Optional: For running tests
pip install unittest  # Usually included with Python
```

## Quick Start

### Using the CLI

```bash
# Run a single task
python cli.py run personal schedule "Team meeting at 10 AM"

# Run tasks from a file
python cli.py batch tasks.example.json

# Check agent statuses
python cli.py status

# Delegate from CEO
python cli.py delegate "Business Agent" analytics "Update revenue metrics"

# Interactive mode
python cli.py interactive
```

### Using Python API

```python
from agent_runner import AgentRunner

runner = AgentRunner()
task = {
    "agent_type": "personal",
    "type": "schedule",
    "event": {"title": "Meeting", "time": "10:00 AM"},
    "description": "Schedule a meeting"
}
result = runner.run_task(task)
```

## Usage

### Basic Usage

```python
from agent_runner import AgentRunner

# Initialize the system
runner = AgentRunner()

# Run a task
task = {
    "agent_type": "personal",
    "type": "schedule",
    "event": {"title": "Meeting", "time": "10:00 AM"},
    "description": "Schedule a meeting"
}

result = runner.run_task(task)
print(result)
```

### Using the CEO Agent

```python
# Delegate tasks through the CEO
runner.delegate_from_ceo(
    task={
        "type": "analytics",
        "metric": "revenue",
        "value": 50000
    },
    target_agent="Business Agent"
)
```

### Batch Processing

```python
tasks = [
    {"agent_type": "personal", "type": "schedule", ...},
    {"agent_type": "business", "type": "analytics", ...},
    {"agent_type": "social", "type": "post", ...}
]

results = runner.run_batch(tasks)
```

## Configuration

Create a `config.json` file (see `config.example.json`):

```json
{
  "log_level": "INFO",
  "ceo": {
    "coordination_mode": "hierarchical"
  },
  "personal": {
    "calendar_sync": true
  },
  "business": {
    "analytics_enabled": true
  },
  "social": {
    "platforms": ["twitter", "linkedin"]
  },
  "autonomous": {
    "learning_enabled": true
  }
}
```

## Examples

Run the examples:

```bash
python examples.py
```

Or run specific examples:

```python
from examples import example_personal_tasks, example_ceo_coordination

example_personal_tasks()
example_ceo_coordination()
```

## Testing

Run the test suite:

```bash
python test_agents.py
```

Or run specific test classes:

```bash
python -m unittest test_agents.TestPersonalAgent
python -m unittest test_agents.TestCEOAgent
```

## Task Types

### Personal Agent Tasks
- `schedule`: Schedule events
- `reminder`: Set reminders
- `communication`: Send messages

### Business Agent Tasks
- `project`: Track projects
- `analytics`: Update metrics
- `decision`: Analyze decisions
- `report`: Generate reports

### Social Agent Tasks
- `post`: Post content
- `engage`: Engage with content
- `network`: Build connections
- `monitor`: Monitor mentions

### CEO Agent Tasks
- `delegate`: Delegate to agents
- `strategy`: Plan strategy
- `coordinate`: Coordinate agents
- `review`: Review performance

### Autonomous Agent Tasks
- `explore`: Explore areas
- `learn`: Learn from data
- `optimize`: Optimize targets
- `autonomous`: Self-directed actions

## Extending the System

### Create a Custom Agent

```python
from base_agent import BaseAgent

class CustomAgent(BaseAgent):
    def __init__(self, config=None):
        super().__init__("Custom Agent", config)

    def process_task(self, task):
        # Implement task processing
        return {"status": "completed", "message": "Task done"}
```

### Register with CEO

```python
custom_agent = CustomAgent()
runner.ceo.register_agent(custom_agent)
```

## License

MIT
