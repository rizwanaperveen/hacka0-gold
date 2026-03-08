# Approve Actions Skill

Process human approvals for sensitive AI Employee actions.

## Description

This skill manages the human-in-the-loop approval workflow by:
1. Checking Approved folder for approved actions
2. Executing approved actions safely
3. Handling rejections appropriately
4. Cleaning up expired approval requests

## Usage

```bash
/approve-actions
```

## What This Skill Does

1. **Scans /Approved folder** for approved action files
2. **Validates approval** (not expired, properly formatted)
3. **Executes the action** based on type:
   - Email sending
   - LinkedIn posting
   - Payment processing
   - File operations
4. **Logs the execution** in Logs folder
5. **Moves completed actions** to Done folder
6. **Cleans up expired requests** from Pending_Approval

## Action Types Supported

### Email Actions
- Send email via Gmail API
- Forward messages
- Reply to threads

### Social Media Actions
- Post to LinkedIn
- Schedule social content
- Respond to messages

### Payment Actions (Gold Tier)
- Process approved payments
- Generate invoices
- Record transactions

### File Actions
- Move/rename files
- Delete files
- Archive documents

## Approval File Format

All approval files must have:
```yaml
---
type: [action_type]
status: pending
created: [timestamp]
expires: [timestamp]
---
```

## Safety Checks

Before executing any approved action:
1. ✓ File is in /Approved folder
2. ✓ Not expired (within 24 hours)
3. ✓ Has valid frontmatter
4. ✓ Action type is recognized
5. ✓ Required parameters present
6. ✓ Passes safety validation

## Workflow

```
Pending_Approval → Human Reviews → Moves to Approved →
/approve-actions skill → Executes → Logs → Moves to Done
```

## Expiration Handling

Approval requests expire after 24 hours:
- Expired requests moved to `/Expired/`
- User notified of expired actions
- Must create new approval request

## Safety Rules

- Only execute actions from /Approved folder
- Validate all parameters before execution
- Log every action with full details
- Never execute expired approvals
- Stop on any validation failure

## Example Flow

1. User moves `EMAIL_client_2026-02-26.md` to /Approved
2. Run `/approve-actions`
3. Skill validates the approval
4. Sends the email
5. Logs the action
6. Moves file to /Done
7. Updates Dashboard
