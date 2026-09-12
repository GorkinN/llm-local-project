---
name: task-breaker
description: Decomposes current task into a plan file with list of tasks and sub-tasks.
---

# Task Breaker

Skill for decomposing complex tasks into structured, actionable plans with sub-tasks. Creates detailed plan files that can guide execution or be assigned to agents.

## Purpose

Break down high-level task descriptions into hierarchical task structures with:
- Clear action items
- Dependencies between tasks
- Estimated complexity levels
- Relevant context and required information

The generated plan file is saved as `PLAN.md` in the current working directory or a specified output directory.

## Usage

### Decompose Task to Plan File

```bash
# Break down current task and save plan
agent "high" 'Generate detailed task breakdown for: {task_description}'
read "{output_file}"  # View generated plan
```

### Examples

#### Simple Task

**Input**: `Research LLM models for local deployment`

**Generated Plan Structure**:
- Research phase (sub-tasks)
- Evaluation phase (sub-tasks)
- Selection criteria (sub-tasks)
- Documentation (sub-tasks)

#### Complex Multi-step Task

**Input**: `Refactor authentication module and implement MFA`

**Generated Plan Structure**:
- Security analysis (sub-tasks)
- Existing auth flow audit (sub-tasks)
- MFA integration design (sub-tasks)
- Implementation (sub-tasks)
- Testing (sub-tasks)
- Documentation (sub-tasks)

#### Technical Task

**Input**: `Optimize database queries for user dashboard`

**Generated Plan Structure**:
- Performance profiling (sub-tasks)
- Query analysis (sub-tasks)
- Index optimization (sub-tasks)
- Caching strategy (sub-tasks)
- Monitoring setup (sub-tasks)

#### Code Review Task

**Input**: `Review pull request for feature branch main`

**Generated Plan Structure**:
- Read and understand PR (sub-tasks)
- Test scenarios design (sub-tasks)
- Code review checklist (sub-tasks)
- Security checks (sub-tasks)
- Feedback formulation (sub-tasks)

#### Research Task

**Input**: `Investigate state-of-the-art computer vision models`

**Generated Plan Structure**:
- Literature review (sub-tasks)
- Model comparison criteria (sub-tasks)
- Reproduction environment setup (sub-tasks)
- Experiment planning (sub-tasks)
- Results analysis (sub-tasks)

## Generated Plan Format

The skill outputs a Markdown file with the following structure:

```markdown
# Task Plan: {original_task}

**Generated**: {timestamp}

## 1. Analysis Phase

| # | Task | Sub-tasks | Complexity | Notes |
|---|------|-----------|------------|-------|
| 1 | Analyze requirements | - Review input task constraints | Medium | ... |

## 2. Implementation Phase

...

## 3. Conclusion

- Summary of tasks
- Resources needed
- Dependencies
```

## Tips for Best Results

### Provide Context

Include relevant details in the task description:
- Project type or domain
- Target audience or users
- Time constraints
- Technical stack
- Available resources

### Examples to Reference

Mention similar completed work or examples to guide breakdown approach.

### Handle Different Complexities

- Simple tasks → 2-3 main steps
- Medium complexity → 5-7 main phases with sub-tasks
- Complex projects → Detailed hierarchical breakdown with milestones

### Use Generated Plans

The output plan can be:
1. Saved and reviewed before execution
2. Used as assignment for agents
3. Compared across different breakdown approaches
4. Converted to checklists or project management formats

---

## Example Session

### Input Task
> Implement a new file upload feature with drag-and-drop support, progress bars, and retry logic for failed uploads. Support multiple file types and size limits per user tier.

### Generated Breakdown
1. **Requirements Analysis** (Complexity: Low)
   - Define supported file types by user tier
   - Specify max file sizes per tier
   - Determine progress bar UI/UX requirements
   
2. **Frontend Implementation** (Complexity: Medium)
   - Design drag-and-drop zone component
   - Implement file validation UI
   - Create progress bar state management
   - Build upload queue visualizer
   
3. **Backend Implementation** (Complexity: High)
   - Design REST API endpoints
   - Implement file storage abstraction
   - Add progress tracking websockets
   - Write retry logic with exponential backoff
   
4. **Testing** (Complexity: Medium)
   - Unit tests for validation logic
   - Integration tests for upload flow
   - E2E tests with drag-drop sequences
   - Performance testing with large files
   
5. **Documentation** (Complexity: Low)
   - API documentation
   - User guide for file limits
   - Troubleshooting common issues

---

## Technical Implementation

The skill leverages Ollama's code generation capabilities to produce high-quality task breakdowns based on the input prompt. Considerations include:

- Analyzing task type (coding, research, analysis, etc.)
- Identifying phases and dependencies
- Estimating complexity for each sub-task
- Handling errors gracefully