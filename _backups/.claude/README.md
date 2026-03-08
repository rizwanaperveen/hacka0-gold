# Multi-Agent System with Skills - Complete Project

A comprehensive multi-agent system with specialized agents and extensible skills for task automation, coordination, and workflow management.

## Project Structure

```
.claude/
├── agents/                    # Multi-agent system (29 files)
│   ├── Core Agents (6)
│   │   ├── base_agent.py
│   │   ├── personal_agent.py
│   │   ├── business_agent.py
│   │   ├── social_agent.py
│   │   ├── ceo_agent.py
│   │   └── autonomous_agent.py
│   │
│   ├── Infrastructure (3)
│   │   ├── agent_runner.py
│   │   ├── main.py
│   │   └── __init__.py
│   │
│   ├── Interfaces (3)
│   │   ├── cli.py
│   │   ├── api_server.py
│   │   └── dashboard.html
│   │
│   ├── Supporting Systems (7)
│   │   ├── database.py
│   │   ├── monitoring.py
│   │   ├── scheduler.py
│   │   ├── notifications.py
│   │   ├── plugins.py
│   │   ├── utils.py
│   │   └── diagnostics.py
│   │
│   └── Documentation & Config (10)
│       ├── README.md
│       ├── QUICKSTART.md
│       ├── INTEGRATION.md
│       ├── PROJECT_STRUCTURE.md
│       ├── CHANGELOG.md
│       ├── test_agents.py
│       ├── examples.py
│       ├── setup.py
│       └── config files...
│
└── skills/                    # Specialized skills (8 files)
    ├── gmail_skill.py
    ├── summarization_skill.py
    ├── social_post_skill.py
    ├── task_creation_skill.py
    ├── logging_skill.py
    ├── audit_skill.py
    ├── __init__.py
    └── README.md
```

## Quick Start

### 1. Setup
```bash
cd .claude/agents
python setup.py
```

### 2. Run Examples
```bash
# Run agent examples
python examples.py

# Run with main launcher
python main.py examples
```

### 3. Start API Server
```bash
python main.py api
# Access at http://localhost:5000
```

### 4. Use CLI
```bash
python main.py cli run personal schedule "Team meeting at 10 AM"
```

### 5. Interactive Mode
```bash
python main.py interactive
```

## Core Components

### Agents (6 specialized agents)

1. **Personal Agent** - Manages personal tasks, schedules, reminders
2. **Business Agent** - Handles business operations, analytics, reports
3. **Social Agent** - Manages social media posting and engagement
4. **CEO Agent** - Coordinates and oversees all other agents
5. **Autonomous Agent** - Self-directed with independent goals
6. **Base Agent** - Foundation class for all agents

### Skills (6 specialized capabilities)

1. **Gmail Skill** - Email management and automation
2. **Summarization Skill** - Text summarization and extraction
3. **Social Post Skill** - Multi-platform social media posting
4. **Task Creation Skill** - Task management across platforms
5. **Logging Skill** - Advanced logging and monitoring
6. **Audit Skill** - Auditing and compliance tracking

## Integration Example

Combining agents and skills for powerful workflows:

```python
from agents.agent_runner import AgentRunner
from skills.gmail_skill import GmailSkill
from skills.task_creation_skill import TaskCreationSkill
from skills.summarization_skill import SummarizationSkill

# Initialize
runner = AgentRunner()
gmail = GmailSkill()
tasks = TaskCreationSkill()
summarizer = SummarizationSkill()

# Workflow: Process unread emails
emails = gmail.read_emails(unread_only=True, max_results=10)

for email in emails:
    # Summarize email content
    summary = summarizer.summarize_text(
        email['snippet'],
        style="concise"
    )

    # Create task via agent
    runner.run_task({
        "agent_type": "personal",
        "type": "schedule",
        "event": {
            "title": f"Reply to: {email['subject']}",
            "time": "2:00 PM"
        },
        "description": summary['summary']
    })

    # Mark email as read
    gmail.mark_as_read([email['id']])

print("Email processing complete!")
```

## Features

### Multi-Agent System
- ✅ 5 specialized agents with distinct capabilities
- ✅ CEO agent for coordination and delegation
- ✅ Task queue management per agent
- ✅ Status tracking and result collection
- ✅ Autonomous agent with self-directed goals

### User Interfaces
- ✅ Command-line interface (CLI)
- ✅ REST API server (Flask)
- ✅ Web dashboard (HTML/JavaScript)
- ✅ Python API for embedding
- ✅ Interactive mode

### Data & Persistence
- ✅ SQLite database for tasks and results
- ✅ Metrics tracking and analytics
- ✅ Audit trail with integrity verification
- ✅ Export to JSON/CSV

### Monitoring & Operations
- ✅ Performance monitoring
- ✅ Health checks and diagnostics
- ✅ Task scheduling
- ✅ Webhook notifications
- ✅ Plugin system

### Skills Library
- ✅ Email automation (Gmail)
- ✅ Text summarization
- ✅ Social media management
- ✅ Task management
- ✅ Advanced logging
- ✅ Audit and compliance

### Deployment
- ✅ Docker support
- ✅ Docker Compose orchestration
- ✅ Production-ready configuration
- ✅ Comprehensive testing

## Usage Examples

### Agent Usage

```python
from agents.agent_runner import AgentRunner

runner = AgentRunner()

# Personal agent - schedule a meeting
runner.run_task({
    "agent_type": "personal",
    "type": "schedule",
    "event": {"title": "Team Standup", "time": "9:00 AM"},
    "description": "Daily standup meeting"
})

# Business agent - update metrics
runner.run_task({
    "agent_type": "business",
    "type": "analytics",
    "metric": "revenue",
    "value": 50000,
    "description": "Update monthly revenue"
})

# Social agent - post to Twitter
runner.run_task({
    "agent_type": "social",
    "type": "post",
    "content": "Exciting product launch! 🚀",
    "platform": "twitter",
    "description": "Announce product launch"
})
```

### Skill Usage

```python
from skills import (
    GmailSkill,
    SummarizationSkill,
    SocialPostSkill,
    TaskCreationSkill
)

# Email automation
gmail = GmailSkill()
gmail.send_email(
    to="team@company.com",
    subject="Weekly Update",
    body="Here's what we accomplished this week..."
)

# Text summarization
summarizer = SummarizationSkill()
summary = summarizer.summarize_text(long_document)
key_points = summarizer.extract_key_points(long_document, num_points=5)

# Social media posting
social = SocialPostSkill()
social.post_to_multiple(
    platforms=["twitter", "linkedin"],
    content="Check out our latest blog post!",
    hashtags=["Tech", "Innovation"]
)

# Task management
tasks = TaskCreationSkill()
tasks.create_task(
    platform="todoist",
    title="Review Q1 results",
    priority="high",
    due_date="2026-03-15"
)
```

### API Usage

```bash
# Start the API server
python main.py api

# Run a task via API
curl -X POST http://localhost:5000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "agent_type": "personal",
    "type": "schedule",
    "description": "Team meeting"
  }'

# Get agent statuses
curl http://localhost:5000/api/agents/status

# Run batch tasks
curl -X POST http://localhost:5000/api/tasks/batch \
  -H "Content-Type: application/json" \
  -d '{"tasks": [...]}'
```

### CLI Usage

```bash
# Run a single task
python main.py cli run personal schedule "Meeting at 10 AM"

# Run batch tasks from file
python main.py cli batch tasks.example.json

# Check system status
python main.py status

# Get system information
python main.py info

# Run diagnostics
python diagnostics.py

# Interactive mode
python main.py interactive
```

## Configuration

Edit `config.json` to customize agent behavior:

```json
{
  "log_level": "INFO",
  "personal": {
    "calendar_sync": true,
    "reminder_interval": 300
  },
  "business": {
    "analytics_enabled": true,
    "report_frequency": "daily"
  },
  "social": {
    "platforms": ["twitter", "linkedin"],
    "auto_post": false
  }
}
```

## Docker Deployment

```bash
# Build and start
docker-compose up -d

# Access services
# API: http://localhost:5000
# Dashboard: http://localhost:8080

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## Testing

```bash
# Run all tests
python test_agents.py

# Run specific test
python -m unittest test_agents.TestPersonalAgent

# Run diagnostics
python diagnostics.py
```

## Documentation

- **README.md** - Main documentation
- **QUICKSTART.md** - 5-minute getting started guide
- **INTEGRATION.md** - API integration examples
- **PROJECT_STRUCTURE.md** - Complete architecture overview
- **CHANGELOG.md** - Version history and changes
- **skills/README.md** - Skills library documentation

## Key Statistics

- **Total Files**: 37 (29 agents + 8 skills)
- **Python Files**: 27
- **Documentation Files**: 6
- **Lines of Code**: ~7,000+
- **Agents**: 6 (5 specialized + 1 base)
- **Skills**: 6 specialized capabilities
- **Interfaces**: 3 (CLI, API, Web)
- **Test Coverage**: Unit tests for all agents

## Dependencies

### Required
```bash
pip install flask flask-cors
```

### Optional
```bash
pip install requests psutil  # For monitoring
pip install google-auth google-api-python-client  # For Gmail
pip install nltk spacy  # For advanced summarization
```

## Architecture Highlights

### Multi-Agent Coordination
- CEO agent delegates tasks to specialized agents
- Each agent has independent task queue
- Results collected and aggregated
- Status tracking across all agents

### Extensibility
- Plugin system for custom functionality
- Skills can be added without modifying core
- Event hooks for integration points
- Webhook support for external notifications

### Production Ready
- Comprehensive error handling
- Structured logging throughout
- Health checks and diagnostics
- Database persistence
- Docker deployment support

## Use Cases

1. **Personal Productivity**
   - Email management and automation
   - Task tracking across platforms
   - Calendar scheduling
   - Reminder management

2. **Business Operations**
   - Project tracking and analytics
   - Report generation
   - Decision support
   - Metrics monitoring

3. **Social Media Management**
   - Multi-platform posting
   - Content scheduling
   - Engagement tracking
   - Brand monitoring

4. **Compliance & Auditing**
   - Audit trail maintenance
   - Security event monitoring
   - Compliance checks
   - Integrity verification

5. **Workflow Automation**
   - Email-to-task conversion
   - Automated reporting
   - Social media campaigns
   - Data processing pipelines

## Next Steps

1. **Customize Agents** - Modify agent behavior for your needs
2. **Add Skills** - Create custom skills for specific tasks
3. **Integrate APIs** - Connect to external services
4. **Deploy** - Use Docker for production deployment
5. **Monitor** - Set up monitoring and alerting
6. **Scale** - Add more agents or distribute workload

## Support & Resources

- Run `python main.py info` for system information
- Run `python diagnostics.py` for health checks
- Check `QUICKSTART.md` for quick setup
- Review `examples.py` for usage patterns
- Read `INTEGRATION.md` for API details

## License

MIT License - See individual files for details

## Version

Current Version: 1.0.0

---

**Built with Python 3.8+ | Flask | SQLite**

**Ready for production deployment with Docker**
