---
name: better-accessibility
description: Enforces WCAG 2.2 AA and AAA accessibility compliance, keyboard navigation focus traps, high-contrast ratios, and ARIA announcement patterns.
---

# `better-accessibility` — Accessible UI Engineering

This skill enforces strict accessibility (a11y) standards across all components, guaranteeing software is usable by everyone, regardless of motor, visual, or cognitive ability.

## Core Rules & Verification

### 1. Color Contrast Standards (WCAG 2.2)
- **Normal Text (< 18pt or < 14pt bold)**: Minimum **4.5:1** contrast ratio against its background.
- **Large Text ($\ge$ 18pt or $\ge$ 14pt bold)**: Minimum **3.0:1** contrast ratio.
- **UI Components & Icons**: Minimum **3.0:1** contrast against adjacent backgrounds.
- Never rely on color alone to convey status (always pair color with an icon or text label).

### 2. Keyboard Navigability & Focus Outlines
- Every interactive element (`<button>`, `<a>`, `<input>`, `<select>`) must be reachable via `Tab`.
- **Never remove focus outlines** without replacing them (`outline: none` without replacement is strictly forbidden).
- Enforce visible, high-contrast focus rings:
  ```html
  class="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
  ```
- **Modal / Dialog Focus Traps**: When a modal opens, focus must be trapped inside. Pressing `Escape` must immediately close the dialog and restore focus to the trigger.

### 3. Screen Reader Semantics & ARIA
- Interactive icon buttons **must** have an `aria-label` or visually hidden text:
  ```html
  <button aria-label="Close dialog"><XIcon /></button>
  ```
- Dynamic updates (toasts, validation errors, live search counts) must use `aria-live="polite"` so screen readers announce changes.
- Accordions and expandable drawers must bind `aria-expanded="true|false"` and `aria-controls="panel-id"`.

### 4. Touch & Click Target Sizing
- Touch targets must be at least **44x44 CSS pixels** on mobile and touch devices.
- For compact desktop controls, ensure target padding expands the clickable hitbox even if the icon is 16px.
