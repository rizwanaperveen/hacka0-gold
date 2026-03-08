You are executing the LinkedIn Post skill for the AI Employee.

## Your Task

Create and post business content on LinkedIn to generate leads and sales.

## Step-by-Step Process

### 1. Read Context
- Read `Business_Goals.md` to understand current business focus
- Read `Company_Handbook.md` for tone and messaging guidelines
- Check `Dashboard.md` for last posting date

### 2. Determine If Posting Is Needed
- Check if enough time has passed since last post (minimum 1 day)
- Verify we haven't exceeded weekly limit (5 posts max)
- If not needed, explain why and exit

### 3. Draft the Post
Create a LinkedIn post that:
- Starts with an attention-grabbing hook
- Addresses a real problem your audience faces
- Offers value (insight, tip, or solution)
- Includes a clear call-to-action
- Uses 3-5 relevant hashtags
- Is 150-300 words (LinkedIn sweet spot)

### 4. Create Approval Request
Write the draft to `/Pending_Approval/LINKEDIN_POST_[timestamp].md` with this format:

```markdown
---
type: linkedin_post
created: [ISO timestamp]
status: pending
expires: [24 hours from now]
---

## Draft Post

[Your drafted post content here]

## Hashtags
#hashtag1 #hashtag2 #hashtag3

## Target Audience
[Who this post is for]

## Expected Outcome
[What you hope to achieve]

## To Approve
Move this file to /Approved folder.

## To Reject
Move this file to /Rejected folder or edit the draft.
```

### 5. Wait for Approval
- Inform the user that the draft is ready for review
- Explain where to find it: `/Pending_Approval/`
- Do NOT proceed to posting until file is in `/Approved/`

### 6. Post to LinkedIn (Only After Approval)
If the file has been moved to `/Approved/`:

1. Start Playwright server if not running:
   ```bash
   bash .claude/skills/browsing-with-playwright/scripts/start-server.sh
   ```

2. Navigate to LinkedIn:
   ```bash
   python3 .claude/skills/browsing-with-playwright/scripts/mcp-client.py call \
     -u http://localhost:8808 -t browser_navigate \
     -p '{"url": "https://www.linkedin.com/feed/"}'
   ```

3. Take snapshot to find "Start a post" button:
   ```bash
   python3 .claude/skills/browsing-with-playwright/scripts/mcp-client.py call \
     -u http://localhost:8808 -t browser_snapshot -p '{}'
   ```

4. Click "Start a post" button (use ref from snapshot)

5. Type the post content

6. Click "Post" button

7. Wait for confirmation

8. Take screenshot of posted content

### 7. Log the Action
Create log entry in `/Logs/[date].json`:
```json
{
  "timestamp": "[ISO timestamp]",
  "action_type": "linkedin_post",
  "actor": "claude_code",
  "status": "success",
  "post_preview": "[First 50 chars of post]",
  "hashtags": ["tag1", "tag2"],
  "approved_by": "human"
}
```

### 8. Update Dashboard
Add to Dashboard.md under Recent Activity:
```
- [YYYY-MM-DD HH:MM] Posted on LinkedIn: "[First line of post]"
```

### 9. Move to Done
Move the approved file from `/Approved/` to `/Done/LINKEDIN_POST_[timestamp].md`

## Important Safety Rules

- NEVER post without approval
- NEVER share confidential client information
- NEVER use aggressive sales language
- ALWAYS maintain professional tone
- ALWAYS include relevant hashtags
- STOP if LinkedIn session is not logged in

## Error Handling

If posting fails:
1. Log the error in `/Logs/[date].json`
2. Move file to `/Needs_Action/FAILED_LINKEDIN_POST_[timestamp].md`
3. Notify user of the failure
4. Do NOT retry automatically

## Success Criteria

- Draft created and approved
- Post successfully published on LinkedIn
- Action logged
- Dashboard updated
- File moved to Done
