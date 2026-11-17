---
name: test-driven-development
description: Mandates a strict Red-Green-Refactor test-driven development loop for spawned worker agents, requiring a failing test before implementation code is authored.
---

# `test-driven-development` — Swarm Worker TDD Protocol

This skill enforces the Test-Driven Development (TDD) cycle for worker agents, guaranteeing that all generated code is provably correct, regression-resistant, and self-documenting.

## The Red-Green-Refactor Cycle

```
  [1. RED] Write failing test -> Verify failure
            |
            v
  [2. GREEN] Write minimal implementation -> Verify pass
            |
            v
  [3. REFACTOR] Clean up code & tokens -> Verify tests still pass
```

### Phase 1: RED (Author Failing Test First)
- Before creating or modifying the implementation file, write a unit or integration test that asserts the requested behavior.
- Run the test suite:
  ```bash
  pytest tests/test_feature.py
  # or
  npm test -- feature.test.ts
  ```
- **Verification Rule**: The test MUST fail, and it must fail for the *expected* reason (e.g., `AssertionError` or `ImportError: cannot import name...`), not due to syntax errors.

### Phase 2: GREEN (Minimal Passing Code)
- Write the minimal code required to satisfy the failing test.
- Do not anticipate unrequested future requirements or write premature abstractions.
- Re-run the test to verify it passes with exit code `0`.

### Phase 3: REFACTOR (Design & Performance Optimization)
- Review the implementation for readability, variable naming, deduplication, and adherence to design tokens.
- Run the entire test suite again to guarantee zero regressions.
