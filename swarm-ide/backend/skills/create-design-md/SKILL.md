---
name: create-design-md
description: Extracts and synthesizes design tokens, typography scales, color palettes, and component conventions into a definitive DESIGN.md specification file.
---

# `create-design-md` — Design System Token Synthesis

Authored by Julien Thibeaut (ibelick), this skill audits a repository, UI codebase, or design reference and codifies its design system into a permanent `DESIGN.md` artifact.

## When to Use
- Starting a multi-worker development task where independent agents need shared design constraints.
- Formalizing an existing frontend without documentation.
- Ensuring consistent styling across different views and pages.

## Synthesis Procedure

1. **Scan Existing Tokens**:
   - Inspect `tailwind.config.js`, `globals.css`, or CSS custom properties.
   - Extract semantic surface, foreground, border, and accent tokens.
2. **Audit Typography**:
   - Detect font families (Sans, Serif, Mono).
   - Document type scale pairings (Display, H1, H2, H3, Body, Small, Code).
3. **Capture Component Invariants**:
   - Standard button variants (`primary`, `secondary`, `destructive`, `ghost`).
   - Card container patterns (padding, border radius, background elevation).
4. **Write `DESIGN.md`**:
   - Generate the file in the workspace root following the standardized specification below.

## Standard `DESIGN.md` Template Structure
```markdown
# Design System Specification

## 1. Color Palette & Semantic Tokens
- **Canvas / Background**: `hsl(var(--background))`
- **Primary Accent**: `hsl(var(--primary))`
- **Card Surface**: `hsl(var(--card))` with subtle `border-border/50`
- **Muted Foreground**: `hsl(var(--muted-foreground))`

## 2. Typography Hierarchy
- **Font Stack**: Sans: Inter / Geist; Mono: JetBrains Mono
- **Headings**: `tracking-tight font-semibold`
- **Body**: `text-sm leading-relaxed text-foreground/90`

## 3. Spatial & Radius Invariants
- **Base Grid**: 4px / 8px increments
- **Container Radius**: `rounded-xl` (12px)
- **Nested Element Radius**: `rounded-lg` (8px)

## 4. Interaction Guidelines
- **Hover**: 150ms ease-out brightness transition
- **Active / Press**: `scale-[0.98]`
- **Focus Rings**: 2px primary ring with 2px offset
```
