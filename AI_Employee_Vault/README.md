# AI Employee Vault - Data Storage Only

**IMPORTANT**: This directory is for DATA ONLY. No code files should be stored here.

## Directory Structure

```
AI_Employee_Vault/
├── Inbox/                 # New items awaiting processing
├── Needs_Action/          # Items requiring action
├── Pending_Approval/      # Items awaiting approval
├── Approved/              # Approved items ready for execution
├── Plans/                 # Approved plans
├── Done/                  # Completed items
├── Rejected/              # Rejected items
├── Expired/               # Expired items
├── data/                  # Structured data storage
├── config/                # Configuration files (JSON/YAML)
├── logs/                  # System logs
├── reports/               # Generated reports
└── watchers/              # Watcher state files
    └── credentials/       # API credentials (gitignored)
```

## Git Configuration

All code has been moved to the main project directories:
- `core/` - Core orchestration and systems
- `agents/` - Decision-making agents
- `skills/` - Atomic executable capabilities
- `integrations/` - External API integrations
- `mcp_servers/` - FastAPI action servers

## .gitignore Rules

```
# Keep all data files
*.*

# But ignore code files
*.py
*.js
*.ts
*.json
*.yaml
*.yml
*.toml

# Except data files
!*.md
!*.txt
!*.csv
!*.log
```

## Access Patterns

- **Read**: Agents and skills read from Inbox, Needs_Action
- **Write**: Agents and skills write to Done, reports, logs
- **Move**: Tasks move through folders as they progress

## Security Notes

- Credentials stored in `watchers/credentials/` are gitignored
- Audit logs are stored in `logs/audit.log`
- Sensitive data should be encrypted at rest
