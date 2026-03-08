#!/bin/bash
# Quick setup script for AI Employee Silver Tier
# Run this after cloning the repository

set -e

echo "🤖 AI Employee Silver Tier Setup"
echo "================================"
echo ""

# Check prerequisites
echo "Checking prerequisites..."

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.9 or higher."
    exit 1
fi
echo "✅ Python 3 found"

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found. Please install Node.js 18 or higher."
    exit 1
fi
echo "✅ Node.js found"

# Check Claude Code
if ! command -v claude &> /dev/null; then
    echo "❌ Claude Code not found. Please install Claude Code CLI."
    exit 1
fi
echo "✅ Claude Code found"

echo ""
echo "Installing dependencies..."

# Install Python dependencies
echo "📦 Installing Python packages..."
cd watchers
pip install -r requirements.txt
playwright install chromium
cd ..

# Install PM2 globally
echo "📦 Installing PM2 process manager..."
npm install -g pm2

# Create directory structure
echo "📁 Creating directory structure..."
mkdir -p AI_Employee_Vault/{Inbox,Needs_Action,Plans,Pending_Approval,Approved,Rejected,Expired,Done,Logs}
mkdir -p watchers/credentials
mkdir -p watchers/sessions
mkdir -p scripts/credentials

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your credentials"
fi

# Create basic vault files if they don't exist
if [ ! -f AI_Employee_Vault/Dashboard.md ]; then
    echo "📝 Creating Dashboard.md..."
    cat > AI_Employee_Vault/Dashboard.md << 'EOF'
# AI Employee Dashboard

Last updated: $(date +%Y-%m-%d)

## Status
🟢 Active

## Recent Activity
- [$(date +%Y-%m-%d)] AI Employee initialized

## Pending Tasks
- Configure watchers
- Set up Gmail API credentials
- Test skills

## Active Plans
None

## Notes
Welcome to your AI Employee! Start by configuring the watchers.
EOF
fi

if [ ! -f AI_Employee_Vault/Company_Handbook.md ]; then
    echo "📝 Creating Company_Handbook.md..."
    cat > AI_Employee_Vault/Company_Handbook.md << 'EOF'
# Company Handbook

## Communication Guidelines

### Email Tone
- Professional but friendly
- Clear and concise
- Always include next steps
- Response time: Within 24 hours for clients

### Social Media
- Post 3-5 times per week on LinkedIn
- Focus on value and insights
- Use 3-5 relevant hashtags
- Maintain professional tone

## Approval Rules

### Requires Approval
- All emails to clients
- All social media posts
- Payments over $50
- File deletions

### Auto-Approve (Future)
- Automated receipts
- Calendar confirmations
- Standard acknowledgments

## Business Hours
Monday-Friday: 9 AM - 6 PM
Response time: Within 24 hours

## Signature
Best regards,
[Your Name]
[Your Title]
[Your Company]
EOF
fi

if [ ! -f AI_Employee_Vault/Business_Goals.md ]; then
    echo "📝 Creating Business_Goals.md..."
    cat > AI_Employee_Vault/Business_Goals.md << 'EOF'
# Business Goals

## Q1 2026 Objectives

### Revenue Target
- Monthly goal: $10,000
- Current MTD: $0

### Key Metrics
- Client response time: < 24 hours
- LinkedIn engagement: 100+ views per post
- Email response rate: > 90%

### Active Projects
1. [Add your projects here]

### Services Offered
- [Add your services here]

### Target Audience
- [Describe your ideal clients]

## Marketing Strategy

### LinkedIn
- Post 3x per week
- Focus on case studies and insights
- Engage with industry content

### Email
- Respond within 24 hours
- Personalized responses
- Clear call-to-action
EOF
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your credentials"
echo "2. Set up Gmail API credentials (see watchers/README.md)"
echo "3. Start watchers: pm2 start watchers/gmail_watcher.py --interpreter python3"
echo "4. Test skills: cd AI_Employee_Vault && claude /process-tasks"
echo ""
echo "📚 Documentation:"
echo "- Silver Tier Setup: SILVER_TIER_SETUP.md"
echo "- Watchers Guide: watchers/README.md"
echo ""
echo "🎉 Happy automating!"
