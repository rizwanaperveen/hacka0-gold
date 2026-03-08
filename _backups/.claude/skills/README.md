# Skills Library

Specialized skills for extending agent capabilities.

## Available Skills

### 1. Gmail Skill (`gmail_skill.py`)
Email management and automation via Gmail API.

**Capabilities:**
- Send emails with attachments
- Read and filter emails
- Mark as read/unread
- Delete emails
- Create drafts
- Search with advanced filters
- Manage labels

**Example:**
```python
from skills.gmail_skill import GmailSkill

gmail = GmailSkill()
gmail.initialize()

# Send an email
gmail.send_email(
    to="recipient@example.com",
    subject="Hello",
    body="This is a test email"
)

# Read unread emails
emails = gmail.read_emails(unread_only=True)
```

### 2. Summarization Skill (`summarization_skill.py`)
Text summarization and content extraction.

**Capabilities:**
- Summarize text in multiple styles (concise, detailed, bullet)
- Extract key points
- Generate TL;DR summaries
- Summarize conversations
- Summarize documents with sections
- Extract topics

**Example:**
```python
from skills.summarization_skill import SummarizationSkill

summarizer = SummarizationSkill()

# Summarize text
result = summarizer.summarize_text(long_text, style="concise")
print(result['summary'])

# Extract key points
points = summarizer.extract_key_points(text, num_points=5)
```

### 3. Social Post Skill (`social_post_skill.py`)
Social media posting and management across platforms.

**Capabilities:**
- Post to multiple platforms (Twitter, LinkedIn, Facebook, Instagram)
- Schedule posts
- Create threads
- Multi-platform posting
- Post analytics
- Delete posts
- Manage scheduled posts

**Example:**
```python
from skills.social_post_skill import SocialPostSkill

social = SocialPostSkill()

# Post to Twitter
social.post_to_platform(
    platform="twitter",
    content="Exciting news! 🚀",
    hashtags=["Tech", "Innovation"]
)

# Schedule a post
social.schedule_post(
    platform="linkedin",
    content="Weekly update",
    scheduled_time="2026-03-04T10:00:00"
)
```

### 4. Task Creation Skill (`task_creation_skill.py`)
Task management across multiple platforms.

**Capabilities:**
- Create tasks on Todoist, Asana, Trello, Jira
- Create subtasks
- Update and complete tasks
- Delete tasks
- Filter and search tasks
- Get overdue tasks
- Create recurring tasks
- Bulk task creation
- Task statistics

**Example:**
```python
from skills.task_creation_skill import TaskCreationSkill

tasks = TaskCreationSkill()

# Create a task
tasks.create_task(
    platform="todoist",
    title="Review proposal",
    due_date="2026-03-10",
    priority="high"
)

# Get overdue tasks
overdue = tasks.get_overdue_tasks()
```

### 5. Logging Skill (`logging_skill.py`)
Advanced logging and monitoring capabilities.

**Capabilities:**
- Log events with metadata
- Log errors with full traceback
- Log metrics
- Log API calls
- Log user actions
- Export logs to JSON/CSV
- Get event summaries
- Metric statistics

**Example:**
```python
from skills.logging_skill import LoggingSkill

logger = LoggingSkill()

# Log an event
logger.log_event(
    event_type="user_action",
    message="User logged in",
    level="info",
    metadata={"user_id": "123"}
)

# Log a metric
logger.log_metric("response_time", 145.5, unit="ms")

# Export logs
logger.export_logs("logs/export.json")
```

### 6. Audit Skill (`audit_skill.py`)
Comprehensive auditing and compliance tracking.

**Capabilities:**
- Log audit events with integrity hashing
- Track access events
- Log data modifications
- Security event monitoring
- Compliance checks (GDPR, HIPAA, SOC2)
- Audit trail with filters
- Verify audit integrity
- Export audit reports

**Example:**
```python
from skills.audit_skill import AuditSkill

auditor = AuditSkill()

# Log access event
auditor.log_access_event(
    user="john.doe",
    resource="/api/users/123",
    access_type="read",
    granted=True
)

# Log security event
auditor.log_security_event(
    event_type="suspicious_activity",
    severity="high",
    description="Multiple failed login attempts"
)

# Verify integrity
integrity = auditor.verify_audit_integrity()
```

## Integration with Agents

Skills can be integrated with agents to extend their capabilities:

```python
from agents.agent_runner import AgentRunner
from skills.gmail_skill import GmailSkill
from skills.task_creation_skill import TaskCreationSkill

# Initialize
runner = AgentRunner()
gmail = GmailSkill()
tasks = TaskCreationSkill()

# Use skills in agent workflows
emails = gmail.read_emails(unread_only=True)

for email in emails:
    # Create a task for each unread email
    tasks.create_task(
        platform="todoist",
        title=f"Reply to: {email['subject']}",
        description=email['snippet']
    )
```

## Creating Custom Skills

To create a custom skill:

1. Create a new Python file in the `skills/` directory
2. Define a class with your skill logic
3. Add initialization and configuration support
4. Implement your skill methods
5. Add example usage

**Template:**
```python
import logging
from typing import Dict, Any

class CustomSkill:
    """Description of your skill."""

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.logger = logging.getLogger("CustomSkill")

    def your_method(self, param: str) -> Dict[str, Any]:
        """Method description."""
        try:
            # Your logic here
            return {"status": "success", "result": "data"}
        except Exception as e:
            self.logger.error(f"Error: {str(e)}")
            return {"status": "error", "error": str(e)}
```

## Configuration

Skills can be configured via the agent configuration file:

```json
{
  "skills": {
    "gmail": {
      "credentials_file": "credentials.json"
    },
    "summarization": {
      "max_summary_length": 500
    },
    "social_post": {
      "platforms": ["twitter", "linkedin"]
    }
  }
}
```

## Dependencies

Some skills may require additional dependencies:

- **Gmail Skill**: `google-auth`, `google-api-python-client`
- **Summarization Skill**: `nltk`, `spacy` (for advanced NLP)
- **Social Post Skill**: Platform-specific SDKs (tweepy, python-linkedin, etc.)

Install with:
```bash
pip install google-auth google-api-python-client
pip install nltk spacy
pip install tweepy python-linkedin
```

## Best Practices

1. **Error Handling**: Always wrap operations in try-except blocks
2. **Logging**: Use the logger for debugging and monitoring
3. **Configuration**: Support configuration via constructor
4. **Return Values**: Return consistent dictionary structures with status
5. **Documentation**: Include docstrings and examples
6. **Testing**: Write unit tests for your skills

## License

MIT
