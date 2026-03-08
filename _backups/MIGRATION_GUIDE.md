# Gold Tier Migration Guide

## 🎯 Overview

This guide provides step-by-step instructions for migrating from Silver Tier to Gold Tier architecture.

## 📋 Pre-Migration Checklist

- [ ] Backup current `.claude` directory
- [ ] Backup `AI_Employee_Vault` directory
- [ ] Document current watchers configuration
- [ ] Export existing task data
- [ ] Note all API credentials and tokens

## 🔄 Migration Steps

### Step 1: Backup Current System

```bash
# Create backup directory
mkdir -p backups/silver_tier_$(date +%Y%m%d)

# Backup .claude directory
cp -r .claude backups/silver_tier_$(date +%Y%m%d)/

# Backup AI_Employee_Vault
cp -r AI_Employee_Vault backups/silver_tier_$(date +%Y%m%d)/

# Backup configuration
cp .env backups/silver_tier_$(date +%Y%m%d)/
cp ecosystem.config.js backups/silver_tier_$(date +%Y%m%d)/
```

### Step 2: Install New Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt

# Install additional packages for Gold Tier
pip install fastapi uvicorn websockets aiohttp asyncio
```

### Step 3: Migrate Existing Skills

The existing skills from `.claude/skills/` need to be reorganized:

**From Silver Tier:**
```
.claude/skills/
├── process-tasks/
├── create-plan/
├── send-email/
├── linkedin-post/
└── approve-actions/
```

**To Gold Tier:**
```
skills/
├── personal/
│   ├── email_skill.py          # Migrated from send-email
│   ├── task_processing_skill.py # Migrated from process-tasks
│   └── planning_skill.py        # Migrated from create-plan
├── business/
│   ├── project_management_skill.py
│   └── reporting_skill.py
├── social/
│   ├── linkedin_skill.py        # Migrated from linkedin-post
│   ├── twitter_skill.py
│   └── facebook_skill.py
└── technical/
    ├── data_processing_skill.py
    └── monitoring_skill.py
```

**Migration Script:**

```python
# scripts/migrate_skills.py
import shutil
from pathlib import Path

def migrate_skills():
    """Migrate Silver Tier skills to Gold Tier structure."""

    # Mapping of old to new locations
    migrations = {
        ".claude/skills/send-email": "skills/personal/email_skill.py",
        ".claude/skills/process-tasks": "skills/personal/task_processing_skill.py",
        ".claude/skills/create-plan": "skills/personal/planning_skill.py",
        ".claude/skills/linkedin-post": "skills/social/linkedin_skill.py",
        ".claude/skills/approve-actions": "core/orchestration/approval_handler.py"
    }

    for old_path, new_path in migrations.items():
        if Path(old_path).exists():
            # Convert skill to Python module
            convert_skill_to_module(old_path, new_path)
            print(f"✓ Migrated {old_path} -> {new_path}")

def convert_skill_to_module(old_path: str, new_path: str):
    """Convert Claude skill to Python module."""
    # Read old skill
    skill_md = Path(old_path) / "SKILL.md"
    if skill_md.exists():
        with open(skill_md, 'r') as f:
            content = f.read()

        # Create new Python module
        # (Implementation would parse the skill and create proper Python code)
        Path(new_path).parent.mkdir(parents=True, exist_ok=True)

        # For now, create placeholder
        with open(new_path, 'w') as f:
            f.write(f'"""Migrated from {old_path}"""\n\n')
            f.write('# TODO: Implement skill logic\n')

if __name__ == "__main__":
    migrate_skills()
```

### Step 4: Migrate Watchers to Integrations

**From Silver Tier:**
```
watchers/
├── gmail_watcher.py
├── whatsapp_watcher.py
└── linkedin_watcher.py
```

**To Gold Tier:**
```
integrations/
├── gmail/
│   ├── __init__.py
│   ├── gmail_client.py      # Core Gmail API client
│   └── gmail_watcher.py     # Migrated watcher logic
├── linkedin/
│   ├── __init__.py
│   ├── linkedin_client.py
│   └── linkedin_watcher.py
└── whatsapp/
    ├── __init__.py
    ├── whatsapp_client.py
    └── whatsapp_watcher.py
```

**Migration Steps:**

1. **Move watcher files:**
```bash
# Gmail
mkdir -p integrations/gmail
cp watchers/gmail_watcher.py integrations/gmail/
cp scripts/gmail_api.py integrations/gmail/gmail_client.py

# LinkedIn
mkdir -p integrations/linkedin
cp watchers/linkedin_watcher.py integrations/linkedin/

# WhatsApp
mkdir -p integrations/whatsapp
cp watchers/whatsapp_watcher.py integrations/whatsapp/
```

2. **Update imports in watcher files:**
```python
# Old import
from scripts.gmail_api import GmailAPI

# New import
from integrations.gmail.gmail_client import GmailClient
```

### Step 5: Migrate AI_Employee_Vault Structure

**Keep existing structure but add new directories:**

```bash
# Create new directories
mkdir -p AI_Employee_Vault/logs
mkdir -p AI_Employee_Vault/data
mkdir -p AI_Employee_Vault/reports
mkdir -p AI_Employee_Vault/config

# Move existing logs
mv AI_Employee_Vault/Logs/* AI_Employee_Vault/logs/ 2>/dev/null || true

# Keep existing folders
# - Needs_Action/
# - Plans/
# - Pending_Approval/
# - Approved/
# - Done/
```

### Step 6: Configure Environment Variables

Update `.env` file with new Gold Tier variables:

```bash
# Copy example
cp .env.example .env

# Add new variables
cat >> .env << 'EOF'

# Gold Tier Configuration
AUTONOMOUS_MODE=true
RALPH_WIGGUM_ENABLED=true
RALPH_WIGGUM_INTERVAL=300

# MCP Servers
PERSONAL_SERVER_PORT=8001
BUSINESS_SERVER_PORT=8002
SOCIAL_SERVER_PORT=8003

# Audit
AUDIT_ENABLED=true
AUDIT_LOG_PATH=AI_Employee_Vault/logs/audit.log

# Cross-Domain
CROSS_DOMAIN_ENABLED=true
EOF
```

### Step 7: Initialize Gold Tier System

```bash
# Run setup script
python scripts/setup_gold_tier.py

# Initialize database
python core/orchestration/init_db.py

# Verify installation
python scripts/verify_installation.py
```

### Step 8: Test Migration

```bash
# Test core orchestrator
python core/orchestration/orchestrator.py

# Test Ralph Wiggum loop (dry run)
python core/autonomous_loop/ralph_wiggum.py --dry-run

# Test agents
python -m pytest tests/test_agents/

# Test integrations
python -m pytest tests/test_integrations/
```

### Step 9: Start Gold Tier System

```bash
# Option 1: Start all components
python scripts/start_all.py

# Option 2: Start individually

# Start MCP servers
python mcp_servers/personal_server/server.py &
python mcp_servers/business_server/server.py &
python mcp_servers/social_server/server.py &

# Start Ralph Wiggum autonomous loop
python core/autonomous_loop/ralph_wiggum.py &

# Start orchestrator
python core/orchestration/orchestrator.py
```

### Step 10: Verify Operation

```bash
# Check system status
python scripts/check_status.py

# View logs
tail -f AI_Employee_Vault/logs/audit.log

# Generate test CEO briefing
python core/orchestration/ceo_briefing.py --period weekly --test
```

## 🔧 Configuration Mapping

### Silver Tier → Gold Tier

| Silver Tier | Gold Tier | Notes |
|-------------|-----------|-------|
| `.claude/skills/` | `skills/{domain}/` | Organized by domain |
| `watchers/` | `integrations/{service}/` | Enhanced with clients |
| `scripts/` | `scripts/` + `core/` | Split into core and utilities |
| `AI_Employee_Vault/` | `AI_Employee_Vault/` | Enhanced structure |
| PM2 processes | Systemd/Docker | Production deployment |

## 📊 Feature Comparison

| Feature | Silver Tier | Gold Tier |
|---------|-------------|-----------|
| Watchers | Manual Python scripts | Integrated API clients |
| Skills | Claude Code skills | Python modules + skills |
| Coordination | Manual | Autonomous orchestrator |
| Error Handling | Basic try/catch | Intelligent recovery |
| Audit | Basic logging | Comprehensive audit trail |
| Cross-Domain | None | Full integration |
| Autonomous | No | Ralph Wiggum loop |
| CEO Briefing | Manual | Automated weekly |
| MCP Servers | None | 3 FastAPI servers |

## 🚨 Common Issues

### Issue 1: Import Errors

**Problem:** `ModuleNotFoundError` after migration

**Solution:**
```bash
# Add project root to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Or add to .env
echo "PYTHONPATH=$(pwd)" >> .env
```

### Issue 2: Credential Migration

**Problem:** API credentials not working

**Solution:**
```bash
# Copy credentials to new location
cp credentials/gmail_credentials.json integrations/gmail/
cp credentials/linkedin_token.json integrations/linkedin/

# Update paths in .env
```

### Issue 3: Database Initialization

**Problem:** Database errors on startup

**Solution:**
```bash
# Initialize database
python core/orchestration/init_db.py

# Or manually
sqlite3 AI_Employee_Vault/data/employee.db < schema.sql
```

## 📝 Post-Migration Tasks

- [ ] Test all integrations
- [ ] Verify autonomous loop operation
- [ ] Generate test CEO briefing
- [ ] Review audit logs
- [ ] Update documentation
- [ ] Train on new CLI commands
- [ ] Set up monitoring dashboards
- [ ] Configure backup schedule

## 🔄 Rollback Procedure

If migration fails:

```bash
# Stop Gold Tier services
python scripts/stop_all.py

# Restore Silver Tier backup
rm -rf .claude
rm -rf AI_Employee_Vault
cp -r backups/silver_tier_YYYYMMDD/.claude .
cp -r backups/silver_tier_YYYYMMDD/AI_Employee_Vault .

# Restart Silver Tier
pm2 restart all
```

## 📞 Support

- Check logs: `AI_Employee_Vault/logs/`
- Run diagnostics: `python scripts/diagnostics.py`
- Review documentation: `docs/`

## ✅ Migration Complete

Once all steps are complete:

1. Verify all tests pass
2. Confirm autonomous loop is running
3. Generate first CEO briefing
4. Monitor for 24 hours
5. Document any custom configurations
6. Update team on new features

---

**Migration Status:** Ready for Production ✅
**Estimated Time:** 2-4 hours
**Difficulty:** Intermediate
