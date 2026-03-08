You are executing the Approve Actions skill for the AI Employee.

## Your Task

Process approved actions from the /Approved folder and execute them safely.

## Step-by-Step Process

### 1. Scan for Approved Actions

Check `/Approved/` folder for files:
```bash
ls -la AI_Employee_Vault/Approved/
```

If empty, report: "No pending approvals to process" and exit.

### 2. Process Each Approved File

For each file in /Approved:

#### A. Read and Validate
```markdown
Read the file and check:
- Has valid YAML frontmatter
- Contains 'type' field
- Contains 'created' timestamp
- Contains 'expires' timestamp
- Status is 'pending' or 'approved'
```

#### B. Check Expiration
```python
from datetime import datetime
expires = datetime.fromisoformat(expires_timestamp)
now = datetime.now()

if now > expires:
    # Move to /Expired/
    # Log expiration
    # Skip execution
    continue
```

#### C. Identify Action Type

Based on the `type` field:
- `email` → Execute email sending
- `linkedin_post` → Execute LinkedIn posting
- `payment` → Execute payment (Gold tier)
- `file_operation` → Execute file operation
- `whatsapp_message` → Execute WhatsApp sending

### 3. Execute Action by Type

#### Email Action
```bash
# Use send-email skill
/send-email --execute-approved "[filename]"
```

Or directly:
1. Extract email parameters (to, subject, body)
2. Send via Gmail API
3. Verify sending
4. Log result

#### LinkedIn Post Action
```bash
# Use linkedin-post skill
/linkedin-post --execute-approved "[filename]"
```

Or directly:
1. Extract post content
2. Use Playwright to post
3. Verify posting
4. Log result

#### Payment Action (Gold Tier)
```bash
# Use payment skill
/process-payment --execute-approved "[filename]"
```

Safety checks:
- Verify amount matches approval
- Verify recipient matches approval
- Double-check account details
- Log before and after execution

#### File Operation Action
```bash
# Execute file operation
# Examples: move, rename, delete, archive
```

Safety checks:
- Verify paths are within allowed directories
- Never delete without backup
- Log operation details

### 4. Log the Execution

For each executed action, create log entry in `/Logs/[date].json`:

```json
{
  "timestamp": "[ISO timestamp]",
  "action_type": "[type]",
  "actor": "claude_code",
  "approval_file": "[filename]",
  "status": "success|failed",
  "details": {
    "specific": "action details"
  },
  "approved_by": "human",
  "approval_timestamp": "[when file moved to Approved]",
  "execution_timestamp": "[when executed]",
  "error": "[if failed]"
}
```

### 5. Update Dashboard

Add to Dashboard.md under Recent Activity:
```markdown
- [YYYY-MM-DD HH:MM] Executed approved action: [brief description]
```

### 6. Move to Done

After successful execution:
```bash
mv "AI_Employee_Vault/Approved/[filename]" "AI_Employee_Vault/Done/[filename]"
```

Update file's frontmatter:
```yaml
status: executed
executed_at: [ISO timestamp]
result: success
```

### 7. Handle Failures

If execution fails:
1. Log the error with full details
2. Move file to `/Needs_Action/FAILED_[filename]`
3. Add error information to file
4. Update Dashboard with failure notice
5. Do NOT retry automatically

### 8. Clean Up Expired Approvals

Check `/Pending_Approval/` for expired requests:
```python
for file in pending_approval_files:
    if is_expired(file):
        move_to_expired(file)
        log_expiration(file)
```

Create summary in Dashboard:
```markdown
## Expired Approvals
- [filename] - expired on [date] - [action type]
```

### 9. Generate Summary Report

After processing all approvals, create summary:

```markdown
## Approval Processing Summary

**Processed:** [count] actions
**Successful:** [count]
**Failed:** [count]
**Expired:** [count]

### Details
- [Action 1]: Success - [brief description]
- [Action 2]: Failed - [error message]
- [Action 3]: Expired - [when expired]
```

## Safety Rules

### Before Execution
- ✓ Validate file is in /Approved (not just named "Approved")
- ✓ Check expiration timestamp
- ✓ Verify all required parameters present
- ✓ Confirm action type is supported
- ✓ Run type-specific safety checks

### During Execution
- Execute one action at a time
- Log before attempting execution
- Capture all output and errors
- Verify success before marking complete

### After Execution
- Always log the result
- Always move file (to Done or Needs_Action)
- Always update Dashboard
- Never leave files in /Approved

## Error Handling

### Invalid Approval File
```
Error: Invalid approval file format
Action: Move to /Needs_Action/INVALID_[filename]
Log: Details of validation failure
```

### Expired Approval
```
Error: Approval expired
Action: Move to /Expired/[filename]
Log: Expiration timestamp
```

### Execution Failure
```
Error: [Specific error message]
Action: Move to /Needs_Action/FAILED_[filename]
Log: Full error details and stack trace
Notify: User via Dashboard
```

### Missing Dependencies
```
Error: Required service not available (e.g., Gmail API)
Action: Keep in /Approved, add note to file
Log: Missing dependency
Notify: User to configure dependency
```

## Success Criteria

- All approved actions processed
- Successful actions logged and moved to Done
- Failed actions logged and moved to Needs_Action
- Expired approvals moved to Expired
- Dashboard updated with summary
- No files left in /Approved folder
