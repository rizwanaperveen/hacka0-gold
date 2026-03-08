# Send Email Skill

Send emails via Gmail with human-in-the-loop approval for sensitive communications.

## Description

This skill enables the AI Employee to:
1. Draft email responses based on context
2. Request approval for sending
3. Send emails via Gmail API or MCP
4. Track sent emails and responses
5. Follow email etiquette rules

## Usage

```bash
/send-email
```

Or with specific recipient:
```bash
/send-email "to: client@example.com, subject: Invoice Follow-up"
```

## What This Skill Does

1. **Reads email context** from Needs_Action folder
2. **Drafts appropriate response** following Company_Handbook tone
3. **Creates approval request** in Pending_Approval folder
4. **Sends email** after human approval
5. **Logs the action** in Logs folder
6. **Updates Dashboard** with email status

## Email Categories

### Auto-Approve (Future Enhancement)
- Automated receipts
- Calendar confirmations
- Standard acknowledgments

### Requires Approval (Current)
- All client communications
- New contact introductions
- Proposals and quotes
- Follow-ups on payments
- Any email with attachments

## Approval Workflow

1. Draft created in `/Pending_Approval/EMAIL_[recipient]_[date].md`
2. Human reviews and can:
   - Approve: Move to `/Approved/`
   - Edit: Modify content, then move to `/Approved/`
   - Reject: Move to `/Rejected/`
3. Skill sends email if approved
4. Email record moved to `/Done/`

## Email Draft Format

```markdown
---
type: email
to: recipient@example.com
cc:
subject: Email Subject
priority: normal
status: pending
created: [timestamp]
expires: [24 hours]
---

## Email Body

[Drafted email content]

## Context
[Why this email is being sent]

## To Approve
Move this file to /Approved folder.

## To Reject
Move this file to /Rejected folder.
```

## Safety Rules

- Never send emails without approval
- Never include sensitive data without encryption
- Always use professional tone
- Follow Company_Handbook communication guidelines
- Verify recipient email addresses
- Include clear subject lines

## Requirements

- Gmail API credentials configured
- Email MCP server running (or Gmail API access)
- Company_Handbook.md with email guidelines
- Proper authentication tokens

## Example Flow

```
Email Request → Draft Response → Pending_Approval →
Human Approves → Send via Gmail → Log & Update Dashboard
```
