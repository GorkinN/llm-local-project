# Task Breakdown Templates

## Template 1: Simple Two-Phase Plan

```markdown
# Task: {TASK_NAME}

## Overview
- **Goal**: {GOAL_DESCRIPTION}
- **Scope**: {SCOPE_BOUNDARIES}  

## Phase 1: Preparation
**Complexity**: {LOW/MEDIUM/HIGH}  
**Duration**: ~{TIME_ESTIMATE} hours

### Tasks:
1. Analyze requirements → Verify constraints and success criteria
2. Setup environment → Install dependencies, configure tools  
3. Design approach → Create initial specifications

### Sub-tasks:
- [ ] Identify specific requirements
- [ ] Review relevant documentation
- [ ] Prepare workspace/tools

## Phase 2: Execution
**Complexity**: {LOW/MEDIUM/HIGH}  
**Duration**: ~{TIME_ESTIMATE} hours

### Tasks:
1. Implement core functionality
2. Add edge case handling
3. Write tests for all features
4. Update documentation
5. Request code review

### Sub-tasks:
- [ ] Complete main implementation
- [ ] Handle error cases  
- [ ] Create test scenarios
- [ ] Document changes made
```

---

## Template 2: Full Project Breakdown

```markdown
# Task: {PROJECT_NAME}

## Summary
**Objective**: Implement complete solution for {OBJECTIVE}

**Dependencies Required**:
- Team members: {LIST}
- Tools/Environment: {TOOLS}
- Access to: {RESOURCES}

**Success Metrics**:
1. Functional requirements met
2. Performance standards achieved  
3. Documentation completed
4. No critical bugs

---

## Phase 1: Discovery & Analysis (5-8h)

### Tasks:
| # | Task Name | Description | Est. Time | Priority |
|---|-----------|-------------|-----------|----------|
| 1 | Requirements Review | Analyze existing system, identify gaps | 2h | High |
| 2 | Stakeholder Interview | Gather needs and expectations | 3h | Medium |
| 3 | Technical Feasibility | Assess technical constraints and options | 3h | High |

### Sub-tasks:
- [ ] Document all known requirements
- [ ] Identify potential blockers
- [ ] Create technical architecture sketch
- [ ] Define acceptance criteria

---

## Phase 2: Design & Planning (8-10h)

### Tasks:
| # | Task Name | Description | Est. Time | Priority |
|---|-----------|-------------|-----------|----------|
| 4 | Architecture | Create detailed system design | 4h | High |
| 5 | Data Model | Define schemas and relationships | 3h | High |
| 6 | API Design | Create endpoints and contracts | 3h | Medium |

### Sub-tasks:
- [ ] Complete UML diagrams  
- [ ] Select appropriate technologies
- [ ] Plan database migrations
- [ ] Review security implications

---

## Phase 3: Implementation (20-40h)

### Tasks breakdown:
- **Core Features** (10-15h)
  - Develop main functionality
  - Implement business logic
  
- **Integration Layer** (3-5h)  <-- Example continuation
  - API endpoint creation
  - External service connections

---

## Phase 4: Testing & QA (8-12h)

### Sub-tasks checklist:
- [ ] Unit tests for all modules
- [ ] Integration tests for flows
- [ ] Performance benchmarking
- [ ] Security scanning and audit
- [ ] User acceptance testing support

---

## Phase 5: Release Preparation (4-6h)

### Tasks:
1. Final validation testing
2. Documentation completion
3. Deployment script preparation
4. Rollback plan documentation
5. Team training materials

---

## Timeline Summary

| Phase | Duration | Start Date | End Date |
|-------|----------|------------|----------|
| Discovery | {PHASE_1_DAYS} days | {START_DATE} | {PHASE1_END_DATE} |
| Design | {PHASE_2_DAYS} days | {DATE} | ... |
```

---

## Template 3: Single-File Component Tasks

```markdown
# Task: {COMPONENT_NAME}

## Context
This task involves working with: {FILE_LOCATION}, {RELATED_COMPONENTS}

---

## Sub-tasks List

### Task 1: Initial Setup (2h)
**Sub-task**: Create base structure
- [ ] Set up component directory
- [ ] Create initial files
- [ ] Add to package exports
**Checklist complete when:** Structure validated and exported correctly

---

### Task 2: Core Logic Implementation (4h)
**Sub-tasks**:
- [ ] Implement primary function
- [ ] Handle basic cases  
- [ ] Document with examples
**Blockers**: {KNOWN_ISSUES}

---

### Task 3: Edge Cases & Error Handling (3h)
**Sub-tasks**:
- [ ] Input validation
- [ ] Error boundary implementation
- [ ] Logging integration
**Blockers**: None known yet

---

## Files Modified
| File | Change Type |
|------|-------------|
| {FILE} | Add/Modify |

## Related Issues
- {ISSUE_LINKS}
```

---

These templates can be referenced when generating plans. They provide consistent formatting that makes it easy to:
- Convert plans to other formats (checklists, tables)
- Track progress against structured checklists  
- Share plans across team members

For the best experience, use the `agent` function with the skill description in mind and let it choose appropriate patterns based on task complexity.
