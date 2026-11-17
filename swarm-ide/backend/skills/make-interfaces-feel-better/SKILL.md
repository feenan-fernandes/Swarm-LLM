---
name: make-interfaces-feel-better
description: Enforces high-craft micro-polish, optical alignment, concentric border radii, layered shadows, scale(0.96) active states, tabular numbers, and smooth spring physics transitions across UI components.
---

# `make-interfaces-feel-better` — Interface Micro-Polish

Authored by Jakub Krehel (Interfaces), this skill codifies the minute design details that elevate generic software into world-class, tactile digital products.

## Core Rules & Principles

### 1. Concentric Border Radii
Never use mismatched nested border radii. The outer radius must equal the inner radius plus the padding between them:
$$R_{\text{outer}} = R_{\text{inner}} + \text{padding}$$
- Bad: Outer container `rounded-2xl` (16px), 8px padding, child button `rounded-2xl` (16px).
- Good: Outer container `rounded-2xl` (16px), 8px padding, child element `rounded-lg` (8px).

### 2. Optical Alignment over Bounding Boxes
Geometry is not perception:
- Icons inside circle buttons: Play icons ($\blacktriangleright$) must be nudged right by 1px–2px to account for triangular visual weight.
- Text beside checkmarks/badges: Align to the font cap-height or baseline, not the raw SVG bounding box.
- Tooltips and badges: Use optical padding (e.g., `py-0.5 px-2` with `text-xs font-medium`).

### 3. Layered Ambient Shadows (Kill Harsh Outlines)
Avoid single opaque 1px black borders or harsh single-stop shadows. Use multi-stop diffuse shadows that simulate real atmospheric light:
```css
/* Subtle elevation */
box-shadow: 
  0 1px 2px 0 rgba(0, 0, 0, 0.05),
  0 4px 6px -1px rgba(0, 0, 0, 0.08),
  inset 0 1px 0 0 rgba(255, 255, 255, 0.15);
```

### 4. Interactive Feedback & Press Physics
Every interactive element must physically respond to human intent:
- **Hover**: Subtle brightness change or background lift (`hover:bg-accent/80`, `transition-all duration-150`).
- **Active / Press**: Tactile compression using `active:scale-[0.97]` or `active:scale-[0.96]` with `transition-transform duration-75`.
- **Focus**: Distinct, non-overlapping focus rings: `focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2`.
- **Minimum Hit Area**: Never make interactive hitboxes smaller than `44x44px` (use invisible pseudo-elements or padding to expand if visual element is smaller).

### 5. Tabular Numbers for Data & Counters
Counters, timers, prices, and statistics must use tabular lining figures to prevent horizontal jitter during updates:
```css
font-variant-numeric: tabular-nums;
/* Tailwind: tabular-nums */
```

### 6. Animation Physics & Timing
- Durations for micro-interactions: **150ms to 250ms**. Anything over 300ms feels sluggish; anything under 100ms feels broken.
- Timing curve: Spring or ease-out: `cubic-bezier(0.16, 1, 0.3, 1)`.
- Staggered entrances: Stagger list item animations by `40ms–60ms` for natural perception.

## Audit Checklist
When reviewing or generating frontend components:
- [ ] Are active states compressed (`scale(0.96)`)?
- [ ] Are numbers set to `tabular-nums`?
- [ ] Are nested radii concentric?
- [ ] Are icons optically centered?
- [ ] Are hit targets at least 44x44px?
- [ ] Are transitions smooth and non-blocking?
