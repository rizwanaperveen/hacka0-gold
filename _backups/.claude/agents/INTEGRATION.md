# API Integration Guide

This guide shows how to integrate the multi-agent system into your applications.

## REST API Integration

### Starting the API Server

```bash
python api_server.py
```

The server will start on `http://localhost:5000`

### API Examples

#### Run a Task

```bash
curl -X POST http://localhost:5000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "agent_type": "personal",
    "type": "schedule",
    "event": {"title": "Meeting", "time": "10:00 AM"},
    "description": "Schedule a meeting"
  }'
```

#### Get Agent Statuses

```bash
curl http://localhost:5000/api/agents/status
```

#### Run Batch Tasks

```bash
curl -X POST http://localhost:5000/api/tasks/batch \
  -H "Content-Type: application/json" \
  -d '{
    "tasks": [
      {
        "agent_type": "personal",
        "type": "schedule",
        "description": "Task 1"
      },
      {
        "agent_type": "business",
        "type": "analytics",
        "description": "Task 2"
      }
    ]
  }'
```

## Python Integration

### Basic Integration

```python
from agents.agent_runner import AgentRunner

# Initialize
runner = AgentRunner()

# Run a task
task = {
    "agent_type": "personal",
    "type": "schedule",
    "event": {"title": "Meeting"},
    "description": "Schedule meeting"
}
result = runner.run_task(task)
```

### Using Utilities

```python
from agents.utils import TaskBuilder, load_config, save_results

# Build a task
task = (TaskBuilder()
    .agent("business")
    .type("analytics")
    .description("Update metrics")
    .param("metric", "revenue")
    .param("value", 50000)
    .build())

# Load configuration
config = load_config("config.json")
runner = AgentRunner(config)

# Run and save results
result = runner.run_task(task)
save_results([result], "results.json")
```

### Monitoring Integration

```python
from agents.agent_runner import AgentRunner
from agents.monitoring import PerformanceMonitor

runner = AgentRunner()
monitor = PerformanceMonitor()

# Run tasks with monitoring
task = {...}
start_time = monitor.metrics.record_task_start("personal", "task-1")
result = runner.run_task(task)
monitor.metrics.record_task_complete("personal", "task-1", start_time, result["status"])

# Check health
health = monitor.check_health(runner)
print(health)

# Get performance report
report = monitor.get_performance_report()
print(report)
```

## JavaScript/TypeScript Integration

### Using Fetch API

```javascript
// Run a task
async function runTask(task) {
  const response = await fetch('http://localhost:5000/api/tasks', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(task),
  });

  return await response.json();
}

// Example usage
const task = {
  agent_type: 'personal',
  type: 'schedule',
  event: { title: 'Meeting', time: '10:00 AM' },
  description: 'Schedule a meeting'
};

runTask(task).then(result => {
  console.log('Task result:', result);
});
```

### Using Axios

```javascript
import axios from 'axios';

const API_BASE = 'http://localhost:5000/api';

// Run a task
async function runTask(task) {
  const response = await axios.post(`${API_BASE}/tasks`, task);
  return response.data;
}

// Get agent statuses
async function getStatuses() {
  const response = await axios.get(`${API_BASE}/agents/status`);
  return response.data;
}

// Run batch tasks
async function runBatch(tasks) {
  const response = await axios.post(`${API_BASE}/tasks/batch`, { tasks });
  return response.data;
}
```

## Environment Variables

Create a `.env` file for configuration:

```env
AGENT_API_HOST=0.0.0.0
AGENT_API_PORT=5000
AGENT_LOG_LEVEL=INFO
AGENT_CONFIG_PATH=config.json
```

## Docker Integration

Create a `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "api_server.py"]
```

Build and run:

```bash
docker build -t multi-agent-system .
docker run -p 5000:5000 multi-agent-system
```

## Error Handling

```python
from agents.agent_runner import AgentRunner
from agents.utils import validate_task

runner = AgentRunner()

task = {
    "agent_type": "personal",
    "type": "schedule",
    "description": "Schedule meeting"
}

# Validate before running
is_valid, error = validate_task(task)
if not is_valid:
    print(f"Invalid task: {error}")
else:
    try:
        result = runner.run_task(task)
        if result.get("status") == "error":
            print(f"Task failed: {result.get('error')}")
        else:
            print(f"Task completed: {result.get('message')}")
    except Exception as e:
        print(f"Exception: {str(e)}")
```

## Webhooks

Set up webhooks to receive notifications:

```python
import requests

def send_webhook(url, data):
    """Send webhook notification."""
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
    except Exception as e:
        print(f"Webhook failed: {str(e)}")

# After task completion
result = runner.run_task(task)
send_webhook("https://your-webhook-url.com", {
    "event": "task_completed",
    "result": result
})
```

## Best Practices

1. **Always validate tasks** before running them
2. **Use monitoring** to track performance
3. **Handle errors gracefully** with try-catch blocks
4. **Set appropriate timeouts** for long-running tasks
5. **Use batch processing** for multiple tasks
6. **Monitor queue sizes** to prevent overload
7. **Clear results periodically** to manage memory
8. **Use configuration files** for environment-specific settings
