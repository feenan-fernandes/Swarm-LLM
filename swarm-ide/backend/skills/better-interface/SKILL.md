---
name: better-interface
description: Orchestrates an exhaustive, multi-domain audit across layout, typography, color tokens, accessibility, copywriting, and component states, producing ranked, file-and-line-cited interface reports.
---

# `better-interface` — Holistic Interface Orchestrator

Authored by Jakub Krehel, `better-interface` coordinates an in-depth review of any user interface or frontend codebase. It prevents shallow "looks good to me" reviews by dispatching an evaluation across 6 distinct sub-disciplines and synthesizing the findings into a prioritized, actionable audit.

## The 6 Evaluation Domains

### 1. Layout & Hierarchy
- Does the page have a clear single focal point per view?
- Is there consistent spatial density across sections?
- Are containers using fluid, responsive wrapping rather than brittle fixed pixel widths?
- Is whitespace intentional (multiples of 4px/8px)?

### 2. Typography & Text Rhythm
- Line length: Are text paragraphs constrained between 50 and 75 characters (`max-w-prose`)?
- Line height: Proportional tracking (tighter line height for large headings, generous 1.5–1.6 for body copy).
- Hierarchy: No more than 3 distinct font sizes visible in any single card or component view.

### 3. Color Tokens & Surface Layering
- Are surfaces utilizing semantic background tokens (`bg-background`, `bg-card`, `bg-popover`) rather than hardcoded hex colors?
- Does dark mode have proper contrast parity without inverted luminance glare?
- Are borders subtle (e.g., `border-border/40`) rather than stark contrast lines?

### 4. Accessibility (WCAG 2.2 AA)
- Color contrast: $\ge 4.5:1$ for body text, $\ge 3:1$ for large headings and icons.
- Keyboard navigation: Full tab stops, visible focus outlines, escape key handling for modals and drawers.
- Semantic HTML: Main landmarks, `<button>` for actions, `<a>` for navigation, proper heading order (`h1` $\rightarrow$ `h2` $\rightarrow$ `h3`).

### 5. Copywriting & Microcopy
- Are button labels action-oriented and unambiguous ("Deploy Project" vs "Submit")?
- Are error messages informative, offering an immediate resolution step?
- Is capitalization consistent across navigation, headers, and badges?

### 6. Component States & Edge Cases
- Every component must gracefully handle:
  - Empty state (clean illustration/message + call to action).
  - Loading state (skeleton screens matching layout dimensions).
  - Error state (inline error banner + retry button).
  - Extreme content (overflow wrapping, long names, high character counts).

## Output Audit Format
When executing `better-interface`, output the findings in this ranked table:

| Severity | Domain | File & Line | Current Behavior | Recommended Fix |
|---|---|---|---|---|
| Critical | A11y | `Button.tsx:24` | Missing focus-visible ring | Add `focus-visible:ring-2 focus-visible:ring-offset-2` |
| Major | Polish | `Card.tsx:12` | Non-concentric outer/inner radius | Set inner child to `rounded-lg` with 8px pad |
| Minor | Copy | `Modal.tsx:45` | Ambiguous label "OK" | Change button label to "Confirm Deletion" |
