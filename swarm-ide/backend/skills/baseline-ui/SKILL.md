---
name: baseline-ui
description: Enforces opinionated frontend constraints, prevents Tailwind anti-patterns, sets transition duration caps, and guarantees mobile-first responsive container layouts.
---

# `baseline-ui` — UI Engineering Constraints

Authored by Julien Thibeaut (ibelick), `baseline-ui` establishes strict engineering boundaries for AI coding agents writing Tailwind CSS, React, Vue, or Web Component interfaces.

## Strict Engineering Constraints

### 1. Tailwind Anti-Pattern Bans
- **No arbitrary fixed heights on text-bearing containers**: Never use `h-[400px]` or `h-64` on containers containing user text or variable feeds; use `min-h-[...]` or `flex-1` with proper overflow management.
- **No pure black or pure white surfaces**: In dark mode, avoid `#000000` (causes optical vibration with white text); use zinc-950/zinc-900 (`#09090b` or `#18181b`). In light mode, avoid stark blinding `#ffffff` on expansive backdrops; use `#fafafa` or stone-50.
- **No arbitrary z-index wars**: Restrict z-index values to structured tiers:
  - Base: `z-0`
  - Sticky / Local: `z-10`
  - Dropdowns / Popovers: `z-30`
  - Fixed Headers / Nav: `z-40`
  - Modals / Dialogs: `z-50`
  - Toast notifications: `z-60`

### 2. Transition Duration Caps
- Micro-interactions (hover, active, toggle): Maximum **200ms** (`duration-200`).
- Modals, drawers, collapse animations: Maximum **300ms** (`duration-300`).
- Anything longer than 300ms must be rejected as sluggish unless explicitly requested as a cinematic showcase.

### 3. Responsive Container Grids
- Avoid `grid-cols-4` without responsive breakpoints.
- Standard pattern: `grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 md:gap-6`.
- Take advantage of container queries (`@container`) for reusable cards that appear in both sidebars and wide body grids.

### 4. Interactive State Completeness
Every interactive element must include explicit classes for:
- Default state
- Hover (`hover:...`)
- Focus (`focus-visible:outline-none focus-visible:ring-2 ...`)
- Active (`active:scale-[0.98]`)
- Disabled (`disabled:opacity-50 disabled:pointer-events-none`)
