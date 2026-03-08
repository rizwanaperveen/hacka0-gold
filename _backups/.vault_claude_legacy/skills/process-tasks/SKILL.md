# Process Tasks Skill

Process tasks from the AI Employee vault's Needs_Action folder.

## Description

This skill enables Claude Code to act as an AI Employee by:
1. Reading tasks from the Needs_Action folder
2. Analyzing them according to Company_Handbook rules
3. Creating action plans
4. Executing approved actions
5. Moving completed tasks to Done folder
6. Updating the Dashboard

## Usage

```bash
/process-tasks
```

## What This Skill Does

1. **Scans Needs_Action folder** for pending tasks
2. **Reads Company_Handbook.md** for decision-making rules
3. **Analyzes each task** and determines priority
4. **Creates a plan** in the Plans folder
5. **Executes safe actions** (reading, organizing, summarizing)
6. **Requests approval** for sensitive actions (emails, payments)
7. **Updates Dashboard.md** with current status
8. **Moves completed tasks** to Done folder

## Task Processing Flow

```
Needs_Action → Analyze → Plan → Execute/Request Approval → Done
```

## Safety Rules

- Never send emails without approval
- Never make payments without approval
- Never delete files without approval
- Always log actions in the Logs folder
- Follow Company_Handbook.md guidelines

## Example

When a file is dropped in Inbox:
1. Watcher creates task in Needs_Action
2. Run `/process-tasks`
3. Claude analyzes the file
4. Creates a plan
5. Executes safe actions or requests approval
6. Updates Dashboard
7. Moves task to Done
