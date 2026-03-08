You are executing the Send Email skill for the AI Employee.

## Your Task

Draft and send emails with human approval, following professional communication standards.

## Step-by-Step Process

### 1. Identify Email Context

Check for email requests in:
- `/Needs_Action/EMAIL_*.md` - Email tasks from watchers
- User-provided context in the command

Read the context to understand:
- Who to email
- What the email is about
- Any previous conversation history
- Urgency level

### 2. Read Guidelines

- Read `Company_Handbook.md` for:
  - Email tone and style
  - Signature format
  - Response time expectations
  - Escalation rules

### 3. Draft the Email

Create a professional email that:
- Has a clear, specific subject line
- Opens with appropriate greeting
- States purpose in first paragraph
- Provides necessary details
- Includes clear call-to-action if needed
- Closes professionally
- Uses company signature

**Email Structure:**
```
Subject: [Clear, specific subject]

Hi [Name],

[Opening - context or acknowledgment]

[Body - main message, 2-3 short paragraphs max]

[Closing - next steps or call-to-action]

[Professional sign-off]
[Your signature from Company_Handbook]
```

### 4. Create Approval Request

Write draft to `/Pending_Approval/EMAIL_[recipient_name]_[timestamp].md`:

```markdown
---
type: email
to: recipient@example.com
cc:
bcc:
subject: [Email subject]
priority: normal
status: pending
created: [ISO timestamp]
expires: [24 hours from now]
in_reply_to: [message_id if replying]
---

## Email Draft

**To:** recipient@example.com
**Subject:** [Subject line]

[Email body content]

---

## Context
[Explain why this email is being sent and what it responds to]

## Attachments
[List any attachments needed, or "None"]

## Expected Response
[What you expect to happen after sending]

## To Approve
Move this file to /Approved folder. You can edit the content before approving.

## To Reject
Move this file to /Rejected folder.
```

### 5. Notify User

Inform the user:
```
Email draft ready for review: /Pending_Approval/EMAIL_[recipient]_[timestamp].md

To approve: Move to /Approved/
To edit: Modify the file, then move to /Approved/
To reject: Move to /Rejected/
```

### 6. Wait for Approval

Do NOT proceed to sending until the file is in `/Approved/` folder.

### 7. Send Email (Only After Approval)

Once approved, send the email using one of these methods:

**Method A: Gmail API (Preferred)**
```python
# Use Gmail API to send
# This requires gmail_api.py helper script
python3 scripts/gmail_api.py send \
  --to "recipient@example.com" \
  --subject "Subject" \
  --body "Body content" \
  --from "your-email@gmail.com"
```

**Method B: Email MCP Server**
```bash
# If email MCP server is configured
python3 scripts/mcp-client.py call \
  -u http://localhost:8809 -t send_email \
  -p '{"to": "recipient@example.com", "subject": "Subject", "body": "Body"}'
```

**Method C: SMTP (Fallback)**
```python
# Use Python smtplib
python3 scripts/send_smtp.py \
  --to "recipient@example.com" \
  --subject "Subject" \
  --body "Body content"
```

### 8. Verify Sending

After sending:
1. Check for success confirmation
2. Capture message ID if available
3. Note timestamp of sending

### 9. Log the Action

Create log entry in `/Logs/[date].json`:
```json
{
  "timestamp": "[ISO timestamp]",
  "action_type": "email_sent",
  "actor": "claude_code",
  "recipient": "recipient@example.com",
  "subject": "[Subject]",
  "status": "success",
  "message_id": "[if available]",
  "approved_by": "human",
  "approval_timestamp": "[when approved]"
}
```

### 10. Update Dashboard

Add to Dashboard.md under Recent Activity:
```
- [YYYY-MM-DD HH:MM] Sent email to [Recipient]: "[Subject]"
```

### 11. Move to Done

Move the approved file from `/Approved/` to `/Done/EMAIL_[recipient]_[timestamp].md`

Update the file's frontmatter:
```yaml
status: sent
sent_at: [ISO timestamp]
```

## Important Safety Rules

- NEVER send emails without approval
- NEVER include passwords or sensitive credentials
- NEVER send to unverified email addresses
- ALWAYS verify recipient before sending
- ALWAYS use professional tone
- STOP if email credentials are not configured

## Email Tone Guidelines

**Professional:**
- Use proper grammar and punctuation
- Avoid slang or overly casual language
- Be concise but complete
- Use active voice

**Friendly but Professional:**
- Warm greeting
- Conversational but respectful
- Show appreciation when appropriate
- End with clear next steps

**Avoid:**
- ALL CAPS (except acronyms)
- Multiple exclamation marks!!!
- Overly long paragraphs
- Jargon without explanation
- Passive-aggressive language

## Error Handling

If sending fails:
1. Log the error with details
2. Move file to `/Needs_Action/FAILED_EMAIL_[recipient]_[timestamp].md`
3. Add error details to the file
4. Notify user of failure
5. Do NOT retry automatically (requires new approval)

## Success Criteria

- Email drafted following guidelines
- Approval obtained from human
- Email successfully sent
- Action logged
- Dashboard updated
- File moved to Done
