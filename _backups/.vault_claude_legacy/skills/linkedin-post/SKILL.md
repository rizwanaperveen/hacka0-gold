# LinkedIn Post Skill

Automatically create and post content on LinkedIn to generate business leads and sales.

## Description

This skill enables the AI Employee to:
1. Draft LinkedIn posts based on business goals
2. Use browser automation to post on LinkedIn
3. Track posting schedule and engagement
4. Generate sales-focused content

## Usage

```bash
/linkedin-post
```

Or with specific topic:
```bash
/linkedin-post "topic: new product launch"
```

## What This Skill Does

1. **Reads Business_Goals.md** to understand current offerings
2. **Checks posting schedule** in Dashboard.md
3. **Drafts a post** focused on business value
4. **Requests approval** via Pending_Approval folder
5. **Posts to LinkedIn** using Playwright automation
6. **Logs the post** in Logs folder
7. **Updates Dashboard** with posting status

## Posting Strategy

- **Frequency**: 3-5 posts per week
- **Best times**: Tuesday-Thursday, 8-10 AM
- **Content types**:
  - Case studies
  - Tips and insights
  - Service announcements
  - Client success stories

## Post Template Structure

```
[Hook - attention grabbing first line]

[Problem statement]

[Your solution/insight]

[Call to action]

#hashtag1 #hashtag2 #hashtag3
```

## Safety Rules

- Always request approval before posting
- Never post sensitive client information
- Follow LinkedIn's posting guidelines
- Maintain professional tone
- Include relevant hashtags (3-5 max)

## Approval Workflow

1. Draft created in `/Pending_Approval/LINKEDIN_POST_[date].md`
2. Human reviews and moves to `/Approved/`
3. Skill executes posting via Playwright
4. Post moved to `/Done/` with engagement tracking

## Example Flow

```
Business_Goals.md → Draft Post → Pending_Approval →
Human Approves → Post to LinkedIn → Log & Update Dashboard
```

## Requirements

- Playwright MCP server running
- LinkedIn account logged in (session saved)
- Business_Goals.md configured
- browsing-with-playwright skill available
