You are executing the Create Plan skill for the AI Employee.

## Your Task

Analyze a complex task and create a detailed, actionable plan.

## Step-by-Step Process

### 1. Identify the Task

Check for tasks in:
- `/Needs_Action/` folder
- User-provided task description
- Dashboard.md pending items

Read the task to understand:
- What needs to be accomplished
- Why it's important
- Any constraints or deadlines
- Who's involved

### 2. Read Context and Guidelines

- Read `Company_Handbook.md` for relevant policies
- Read `Business_Goals.md` for alignment
- Check `Dashboard.md` for related ongoing work
- Review similar completed tasks in `/Done/`

### 3. Analyze Task Complexity

Determine if this task needs a plan:
- **Simple** (1-2 steps): No plan needed, just execute
- **Moderate** (3-5 steps): Create basic plan
- **Complex** (6+ steps): Create detailed plan with dependencies

If simple, inform user and suggest direct execution instead.

### 4. Break Down Into Steps

Decompose the task into clear, actionable steps:

**Good steps:**
- "Draft email response to client inquiry"
- "Research competitor pricing for Q1 report"
- "Schedule meeting with team for project kickoff"

**Bad steps:**
- "Handle the email" (too vague)
- "Do research" (no clear output)
- "Fix everything" (not specific)

Each step should:
- Start with an action verb
- Have a clear deliverable
- Be completable in one session
- Have measurable success criteria

### 5. Identify Dependencies

Map out what must happen before each step:
```
Step 1: Gather requirements → No dependencies
Step 2: Draft proposal → Depends on Step 1
Step 3: Get approval → Depends on Step 2
Step 4: Send to client → Depends on Step 3
```

### 6. Assess Risks

Think about what could go wrong:
- Missing information or access
- External dependencies (other people)
- Technical limitations
- Time constraints
- Approval delays

For each risk, provide mitigation strategy.

### 7. Create the Plan File

Write to `/Plans/PLAN_[task_name]_[timestamp].md`:

```markdown
---
type: plan
task_id: [original task filename if from Needs_Action]
created: [ISO timestamp]
status: draft
priority: normal
estimated_effort: [X hours or Y days]
---

# Plan: [Clear, Descriptive Title]

## Objective
[One paragraph: What are we trying to achieve and why?]

## Context
[Background information, why this task exists, who requested it]

## Steps

### Step 1: [Action Verb + Clear Description]
- **What**: [Detailed explanation of this step]
- **How**: [Method, tool, or approach to use]
- **Output**: [What will exist after this step]
- **Dependencies**: None
- **Estimated time**: [X hours]
- **Requires approval**: No

### Step 2: [Next Action]
- **What**: [Description]
- **How**: [Method]
- **Output**: [Deliverable]
- **Dependencies**: Step 1 must be complete
- **Estimated time**: [X hours]
- **Requires approval**: Yes - [explain why]

[Continue for all steps...]

## Resources Needed
- [File path or document name]
- [Tool or system access]
- [Information from specific person]
- [Credentials or permissions]

## Risks & Mitigation

### Risk 1: [Potential problem]
- **Likelihood**: Low/Medium/High
- **Impact**: Low/Medium/High
- **Mitigation**: [How to prevent or handle]

### Risk 2: [Another potential problem]
- **Likelihood**: [Level]
- **Impact**: [Level]
- **Mitigation**: [Strategy]

## Success Criteria
- [ ] [Measurable outcome 1]
- [ ] [Measurable outcome 2]
- [ ] [Measurable outcome 3]

## Next Actions
1. [Immediate first step to take]
2. [What comes after that]

## Notes
[Any additional context, assumptions, or considerations]
```

### 8. Link Related Resources

In the plan, reference relevant files:
- Link to Company_Handbook sections
- Link to related tasks in Done folder
- Link to Business_Goals if applicable
- Link to any templates or examples

Use relative paths:
```markdown
See [Email Guidelines](../Company_Handbook.md#email-guidelines)
Reference [Similar Project](../Done/PROJECT_example.md)
```

### 9. Update Dashboard

Add to Dashboard.md:
```markdown
## Active Plans
- [YYYY-MM-DD] [Plan Title](Plans/PLAN_[name]_[timestamp].md) - Status: Draft
```

### 10. Notify User

Inform the user:
```
Plan created: /Plans/PLAN_[name]_[timestamp].md

Summary:
- [X] steps identified
- Estimated effort: [Y hours/days]
- [Z] steps require approval
- [N] risks identified

Next: Review the plan, then run /process-tasks to begin execution.
```

## Planning Best Practices

### For Email Tasks
- Step 1: Read context and history
- Step 2: Draft response
- Step 3: Request approval
- Step 4: Send email
- Step 5: Log and file

### For Content Creation
- Step 1: Research topic
- Step 2: Draft content
- Step 3: Review against guidelines
- Step 4: Request approval
- Step 5: Publish
- Step 6: Track engagement

### For Multi-Domain Tasks
- Group steps by domain (email, social, files)
- Identify handoff points
- Plan for approval at domain boundaries
- Include verification steps

## Estimation Guidelines

**Simple tasks** (1-2 hours):
- Single email response
- Basic file organization
- Simple data entry

**Moderate tasks** (3-8 hours):
- Multi-step email thread
- Content creation with research
- Report generation

**Complex tasks** (1-3 days):
- Project proposals
- Multi-channel campaigns
- System integrations

**Major initiatives** (1+ weeks):
- Quarterly planning
- Process redesign
- New service launch

## Safety Rules

- Never create plans for illegal or unethical tasks
- Flag any steps that seem risky or unusual
- Always include approval steps for sensitive actions
- Document assumptions clearly
- Include rollback procedures for risky steps

## Error Handling

If task is unclear:
1. Document what's unclear in the plan
2. Create a step: "Clarify requirements with user"
3. Mark plan status as "needs_clarification"
4. Notify user of questions

If task is too complex:
1. Break into multiple sub-plans
2. Create a master plan that links to sub-plans
3. Prioritize which sub-plan to tackle first

## Success Criteria

- Plan is clear and actionable
- Each step has measurable output
- Dependencies are mapped correctly
- Risks are identified with mitigations
- Effort is estimated reasonably
- Plan file created in /Plans folder
- Dashboard updated
- User notified with summary
