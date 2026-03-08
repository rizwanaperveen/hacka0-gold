# Quick Start Guide

Get the multi-agent system running in 5 minutes.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Installation

### Option 1: Local Installation

```bash
# 1. Navigate to the agents directory
cd .claude/agents

# 2. Install dependencies (optional, for API server)
pip install -r requirements.txt

# 3. Run your first task
python cli.py run personal schedule "Team meeting at 10 AM"
```

### Option 2: Docker Installation

```bash
# 1. Build and start containers
docker-compose up -d

# 2. Access the dashboard
# Open http://localhost:8080 in your browser

# 3. API is available at http://localhost:5000
```

## Basic Usage

### Using the CLI

```bash
# Run a single task
python cli.py run personal schedule "Team meeting"

# Run tasks from a file
python cli.py batch tasks.example.json

# Check agent statuses
python cli.py status

# Interactive mode
python cli.py interactive
```

### Using Python

```python
from agent_runner import AgentRunner

# Initialize
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

### Using the API

```bash
# Start the API server
python api_server.py

# In another terminal, run a task
curl -X POST http://localhost:5000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "agent_type": "personal",
    "type": "schedule",
    "description": "Team meeting"
  }'
```

### Using the Dashboard

1. Start the API server: `python api_server.py`
2. Open `dashboard.html` in your browser
3. Use the web interface to run tasks and monitor agents

## Example Tasks

### Personal Agent

```python
# Schedule an event
task = {
    "agent_type": "personal",
    "type": "schedule",
    "event": {"title": "Doctor Appointment", "time": "2:00 PM"},
    "description": "Schedule appointment"
}

# Set a reminder
task = {
    "agent_type": "personal",
    "type": "reminder",
    "reminder": {"text": "Buy groceries", "time": "6:00 PM"},
    "description": "Set reminder"
}
```

### Business Agent

```python
# Track a project
task = {
    "agent_type": "business",
    "type": "project",
    "project": {"name": "Q1 Launch", "status": "in_progress"},
    "description": "Track project"
}

# Update analytics
task = {
    "agent_type": "business",
    "type": "analytics",
    "metric": "revenue",
    "value": 50000,
    "description": "Update revenue"
}
```

### Social Agent

```python
# Post to social media
task = {
    "agent_type": "social",
    "type": "post",
    "content": "Exciting news!",
    "platform": "twitter",
    "description": "Post update"
}

# Monitor mentions
task = {
    "agent_type": "social",
    "type": "monitor",
    "keywords": ["brand_name", "product"],
    "description": "Monitor mentions"
}
```

### CEO Agent (Coordination)

```python
# Delegate to another agent
runner.delegate_from_ceo(
    task={
        "type": "analytics",
        "metric": "users",
        "value": 10000
    },
    target_agent="Business Agent"
)
```

### Autonomous Agent

```python
# Set a goal
autonomous = runner.agents["autonomous"]
autonomous.set_goal({
    "description": "Optimize system performance",
    "priority": "high"
})

# Run autonomous tasks
task = {
    "agent_type": "autonomous",
    "type": "explore",
    "area": "system_metrics",
    "description": "Explore metrics"
}
```

## Running Examples

```bash
# Run all examples
python examples.py

# Run tests
python test_agents.py
```

## Configuration

Create a `config.json` file (see `config.example.json`):

```json
{
  "log_level": "INFO",
  "personal": {
    "calendar_sync": true
  },
  "business": {
    "analytics_enabled": true
  }
}
```

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check [INTEGRATION.md](INTEGRATION.md) for API integration examples
- Explore the example tasks in `tasks.example.json`
- Customize agent behavior by editing the agent files

## Troubleshooting

### Import Errors

If you get import errors, make sure you're in the correct directory:

```bash
cd .claude/agents
python -c "from agent_runner import AgentRunner; print('OK')"
```

### API Server Won't Start

Make sure Flask is installed:

```bash
pip install flask flask-cors
```

### Database Issues

Delete the database file to reset:

```bash
rm agents.db
```

## Getting Help

- Check the [README.md](README.md) for full documentation
- Review [examples.py](examples.py) for usage patterns
- Run tests to verify installation: `python test_agents.py`

## What's Next?

Now that you have the system running, you can:

1. **Customize agents** - Edit agent files to add your own logic
2. **Add integrations** - Connect to external APIs and services
3. **Build workflows** - Chain multiple agents together
4. **Monitor performance** - Use the monitoring tools to track metrics
5. **Scale up** - Deploy with Docker for production use
