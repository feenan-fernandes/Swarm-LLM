---
name: requesting-code-review
description: Standardizes the handoff protocol when worker agents delegate code changes, PR diffs, and verification steps to reviewer subagents without polluting context windows.
---

# `requesting-code-review` — Multi-Agent Review Protocol

In a swarm or multi-agent system, the root orchestrator must delegate verification to dedicated reviewer subagents. This skill defines the structured handoff contract used when spawning a reviewer worker.

## The Review Handoff Contract

When a worker agent finishes drafting a feature or bugfix, it MUST package its review request using the following schema before calling `<spawn_worker>` or requesting review:

```markdown
### Review Request Handoff
1. **Goal Summary**: Brief 1-2 sentence description of what the change accomplishes.
2. **Key Files Modified**:
   - `path/to/file.ts`: Description of functional changes.
3. **5-Axis Assessment Target**:
   - **Correctness**: Does it meet all prompt requirements without edge-case regressions?
   - **Simplicity**: Is there dead code, over-engineering, or accidental bloat?
   - **Architecture**: Does it adhere to project conventions and design token standards?
   - **Security**: Are inputs sanitized and secrets protected?
   - **Performance**: Are there unmemoized loops, heavy re-renders, or unindexed queries?
4. **Verification Evidence**:
   - Command used to run tests: `npm test` or `pytest ...`
   - Test output summary: Exit code, tests passed, tests failed.
5. **Known Limitations / Follow-ups**: Any out-of-scope items left untouched.
```

## Reviewer Agent Output Format
The receiving reviewer agent evaluates the code against the 5 axes and replies with:
- **Verdict**: `APPROVED`, `REQUEST_CHANGES`, or `BLOCKED`.
- **Ranked Findings**: Table of critical, major, and minor issues with line numbers.
- **Specific Fix Diffs**: Contiguous drop-in diffs for any requested changes.
