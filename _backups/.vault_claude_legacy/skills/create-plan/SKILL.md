# Create Plan Skill

Generate structured action plans for complex tasks using Claude's reasoning capabilities.

## Description

This skill enables the AI Employee to:
1. Analyze complex tasks from Needs_Action
2. Break them down into actionable steps
3. Create detailed Plan.md files
4. Identify dependencies and risks
5. Estimate effort and timeline

## Usage

```bash
/create-plan
```

Or for a specific task:
```bash
/create-plan "task: prepare Q1 tax documents"
```

## What This Skill Does

1. **Reads task** from Needs_Action or user input
2. **Analyzes complexity** and requirements
3. **Breaks down into steps** with clear actions
4. **Identifies dependencies** between steps
5. **Creates Plan.md** in Plans folder
6. **Links to relevant resources** in the vault
7. **Updates Dashboard** with plan status

## Plan Structure

Each plan includes:
- **Objective**: Clear goal statement
- **Context**: Background and why this matters
- **Steps**: Numbered, actionable tasks
- **Dependencies**: What needs to happen first
- **Resources**: Files, tools, or information needed
- **Risks**: Potential blockers or issues
- **Success Criteria**: How to know it's done

## When to Create Plans

Create plans for tasks that:
- Involve multiple steps (3+)
- Require coordination across domains
- Have dependencies or prerequisites
- Need approval at multiple stages
- Are time-sensitive or complex

## Plan File Format

```markdown
---
type: plan
task_id: [original task filename]
created: [timestamp]
status: draft
priority: normal|high|urgent
estimated_effort: [hours or days]
---

# Plan: [Task Title]

## Objective
[Clear statement of what we're trying to achieve]

## Context
[Why this task exists, background information]

## Steps

### Step 1: [Action]
- **What**: [Detailed description]
- **How**: [Method or approach]
- **Output**: [Expected result]
- **Dependencies**: [None or list]
- **Estimated time**: [X hours/days]

### Step 2: [Action]
[Same structure]

## Resources Needed
- [File, tool, or information]
- [Access or credentials]

## Risks & Mitigation
- **Risk**: [Potential issue]
  - **Mitigation**: [How to handle it]

## Success Criteria
- [ ] [Measurable outcome 1]
- [ ] [Measurable outcome 2]

## Next Actions
1. [Immediate next step]
2. [Following step]
```

## Integration with Other Skills

Plans created by this skill are used by:
- `/process-tasks` - Executes plan steps
- `/approve-actions` - Handles approval steps
- `/send-email` - Sends communications in plan
- `/linkedin-post` - Posts content as planned

## Example Flow

```
Complex Task → /create-plan → Plan.md created →
/process-tasks reads plan → Executes steps → Updates plan status
```

## Safety Rules

- Plans are drafts until reviewed
- Mark steps requiring approval clearly
- Include rollback procedures for risky steps
- Link to Company_Handbook for guidelines
- Update plan status as steps complete

## Success Criteria

- Plan is clear and actionable
- All steps have success criteria
- Dependencies are identified
- Risks are documented
- Plan saved in /Plans folder
- Dashboard updated with plan link
