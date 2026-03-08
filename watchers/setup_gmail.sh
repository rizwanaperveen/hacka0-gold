#!/bin/bash

# Gmail API Setup Helper Script
# This script guides you through setting up Gmail API credentials

echo "============================================================"
echo "Gmail API Setup Helper"
echo "============================================================"
echo ""

# Check if credentials directory exists
CREDS_DIR="credentials"
CREDS_FILE="$CREDS_DIR/gmail_credentials.json"

if [ ! -d "$CREDS_DIR" ]; then
    echo "Creating credentials directory..."
    mkdir -p "$CREDS_DIR"
fi

# Check if credentials file exists
if [ -f "$CREDS_FILE" ]; then
    echo "✅ Credentials file found: $CREDS_FILE"
    echo ""
    echo "Testing credentials..."
    python test_gmail_credentials.py
else
    echo "❌ Credentials file not found: $CREDS_FILE"
    echo ""
    echo "============================================================"
    echo "SETUP INSTRUCTIONS"
    echo "============================================================"
    echo ""
    echo "Step 1: Go to Google Cloud Console"
    echo "  → https://console.cloud.google.com/"
    echo ""
    echo "Step 2: Create a new project"
    echo "  → Click 'Select a project' → 'New Project'"
    echo "  → Name: 'AI-Employee-Gmail'"
    echo "  → Click 'Create'"
    echo ""
    echo "Step 3: Enable Gmail API"
    echo "  → Search for 'Gmail API'"
    echo "  → Click 'Enable'"
    echo ""
    echo "Step 4: Create OAuth Credentials"
    echo "  → Go to 'APIs & Services' → 'Credentials'"
    echo "  → Click 'Create Credentials' → 'OAuth client ID'"
    echo "  → Configure consent screen if prompted:"
    echo "    - User Type: External"
    echo "    - App name: AI Employee"
    echo "    - Add your email as test user"
    echo "  → Application type: Desktop app"
    echo "  → Name: AI Employee Desktop"
    echo "  → Click 'Create'"
    echo ""
    echo "Step 5: Download credentials"
    echo "  → Click 'Download JSON'"
    echo "  → Save the file as:"
    echo "    $CREDS_FILE"
    echo ""
    echo "Step 6: Run this script again"
    echo "  → bash setup_gmail.sh"
    echo ""
    echo "============================================================"
    echo ""
    echo "For detailed instructions, see: credentials/README.md"
    echo ""
fi
