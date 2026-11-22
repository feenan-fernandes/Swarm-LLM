---
name: writing-plans
description: Decomposes complex user requests into bite-sized 2-5 minute actionable implementation tasks with explicit file paths, test commands, and verification criteria before writing any code.
category: productivity
author: obra
tags:
  - planning
  - task-decomposition
  - specifications
  - execution-plans
---

# Writing Implementation Plans

Never begin modifying code on a non-trivial feature or refactor without a concrete, file-by-file implementation plan.

---

## 1. Core Principles

- **Bite-Sized Chunks:** Break tasks down into units that take 2–5 minutes of agent execution each.
- **YAGNI (You Aren't Gonna Need It):** Build strictly what is needed to satisfy the request; never speculative future-proofing.
- **DRY (Don't Repeat Yourself):** Reuse existing abstractions and conventions found in the codebase.
- **TDD Integration:** Every task modifying functionality must specify the exact test file to create or update and the command to verify it.
- **Explicit File Mapping:** State exact relative paths for every file created or edited.

---

## 2. Structure of an Implementation Plan

Every generated plan should follow this standard structure:

### Phase 1: Exploration & Setup
- Identify target files and existing dependencies.
- Confirm baseline test suite runs cleanly.

### Phase 2: Implementation Milestones (Task-by-Task)
For each milestone:
```markdown
### Task N: [Concise Title]
- **Target Files:** `src/models/user.py`, `tests/test_user.py`
- **Action:** Create failing test for user authentication validation.
- **Verification Command:** `pytest tests/test_user.py -k test_auth`
- **Expected Outcome:** Fails with `AttributeError` (Red).
- **Implementation:** Implement minimal `validate_credentials()` method.
- **Re-Verification:** `pytest tests/test_user.py -k test_auth` passes with exit code 0 (Green).
```

### Phase 3: Regression & Polish
- Full test suite run (`pytest`, `npm test`).
- Static analysis & lint checks (`ruff check`, `mypy`, `py_compile`).
- Verification gate checklist (`verification-before-completion`).

---

## 3. Strict Rules

1. **Announce Plan Creation:** Always output `<plan>` or write the plan to disk before touching code.
2. **Never Lump Everything Together:** Never write "Task 1: Build the backend and frontend". Separate concerns into discrete, verifiable milestones.
3. **Pass Criteria:** Every task must have a measurable, command-line verifiable pass/fail condition.
