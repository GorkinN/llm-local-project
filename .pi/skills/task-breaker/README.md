# Task Breaker Skill

A skill for decomposing complex tasks into structured, actionable plans.

## Overview

This skill helps break down high-level task descriptions into hierarchical task structures with:
- **Main phases** - Logical groupings of work
- **Sub-tasks** - Specific action items within each phase  
- **Complexity indicators** - Low/Medium/High estimates
- **Dependencies** - Which tasks must complete before others
- **Resources needed** - Tools, teams, or materials required

## How It Works

When invoked, the task-breaker skill:

1. **Analyzes** the input task description
2. **Identifies** key phases and sub-tasks
3. **Determines** dependencies between tasks
4. **Estimates** complexity for each item
5. **Generates** a structured plan file (PLAN.md)

## Usage Examples

### Basic Task Breakdown

```bash
# Pass task description to agent, requesting breakdown
agent "high" 'Break down this task into a detailed plan with sub-tasks: {task_description}'
read "{output_file}"  # View generated PLAN.md
```

### Specific Task Types

#### Coding Tasks
```
Implement file upload feature with drag-and-drop and progress tracking
```

#### Research Tasks  
```
Investigate LLM models suitable for local deployment on limited hardware
```

#### Refactoring Tasks
```
Refactor authentication module to support multiple providers
```

#### Documentation Tasks
```
Create API documentation for new project endpoints
```

## Generated Plan File Format

Each plan is generated as a Markdown document (`PLAN.md`) containing:

```markdown
# Task Breakdown Plan

## Original Task
{task description}

## Overview
- Primary objective
- Main deliverables
- Success criteria

## Phases

### Phase 1: {Phase Name}
**Complexity**: Medium
**Estimated Duration**: 4-8 hours
**Dependencies**: None
**Required Resources**: Code editor, testing environment

#### Tasks
1. Task description one
2. Task description two

##### Sub-tasks
- Specific action item A
- Specific action item B
```

## Phase Breakdown Patterns

The skill creates plans based on task type:

### Technical/Implementation Tasks
- Requirements analysis
- Architecture/design phase
- Implementation phases (breaking into logical modules)
- Testing and validation
- Documentation

### Research/Investigation Tasks
- Literature survey
- Method setup
- Data collection
- Analysis phase
- Report writing

### Debugging/Maintenance Tasks
- Problem analysis
- Root cause investigation
- Solution design
- Implementation/testing
- Validation/regression testing

---

## Best Practices

1. **Provide Context**: Include project details, constraints, and preferences
2. **Be Honest About Scope**: Describe the full task, not just parts you want skipped
3. **Mention Deadlines**: Time pressures help prioritize appropriately
4. **Specify Preferences**: Note any tools or approaches to use/avoid

## Tips for Users

- Use with `agent "high"` prompt for best results
- Review generated plan before starting work
- Adjust complexity estimates after initial execution
- Share plans with team members for coordination

---

## Related Skills

- `code-generator`: For actual code generation based on broken-down tasks
- `bash`: For executing commands listed in task sub-tasks
- `read`: For accessing project files mentioned in plans

---

## Example Session

```bash
# Task: Create a new feature branch with comprehensive PR template
agent "high" 'Break down this task into steps with sub-tasks'
read plan.md
# Now execute the plan step by step or assign to agents
```

The generated markdown file can be converted to:
- Jira issues using `/api/api/v2.0/jira/issue/{PROJECT}/{ISSUE}` calls
- GitHub labels and project boards
- Checklists (using checkboxes like `- [ ] task name`)