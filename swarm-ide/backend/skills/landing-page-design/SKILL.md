---
name: landing-page-design
description: Structured blueprint to build high-converting, uniquely styled landing pages and marketing sites without generic AI slop. Enforces strategic intake, one-offer hierarchy, conversion copywriting, strict token scales (typography, spacing, radius), and anti-cliche guardrails.
category: interface
author: elayadesign
tags:
  - landing-page
  - design
  - marketing
  - conversion
  - typography
  - ux-ui
---

# Landing Page Design System & Workflow

A landing page is **not** a homepage. A landing page exists for **one offer → one audience → one primary action**.
Never generate generic templates, stock AI buzzwords ("Seamless", "Elevate", "Game changer"), or uncurated layouts.

---

## PART A — STRATEGY & STRUCTURE (DO THIS FIRST)

Never jump straight into coding visual UI before completing Part A.

### A1. Structured Intake
Gather these requirements before writing any code or copy. If missing, ask in a single unified prompt or make explicit reasonable assumptions:
1. **Purpose:**
   - **One primary action:** Trial, demo, purchase, waitlist, or download.
   - **Exact offer:** What tangible deliverable does the user receive?
   - **Conversion trigger:** Button click, email input, or checkout.
2. **Audience & Context:**
   - **ICP (Ideal Customer Profile):** Who are they and what urgent pain do they suffer?
   - **Top 3 Objections:** Why do prospects bounce without converting today?
   - **Traffic Source:** Organic search, cold ads, social referral, or newsletter.
3. **Proof Assets:**
   - Available customer logos, metrics, verbatim quotes, demo recordings, or case studies.
4. **Constraints:**
   - Brand tone (serious enterprise, punchy developer, warm consumer), existing color palettes, mobile priority.

---

### A2. Page Architecture (The Conversion Spine)
A conversion-optimized landing page strictly flows through this sequence:
1. **Hero Section:** High-contrast hook + immediate value proposition + primary CTA + friction killer.
2. **Proof Bar:** Verified customer logos, ratings, or active user metrics directly below the fold hook.
3. **Problem / Agitation:** Explicitly articulate the painful status quo before offering the antidote.
4. **Solution Overview:** Introduce your product as the direct, friction-free transformation.
5. **How It Works (Exactly 3 Steps):** Step 1 (Setup) → Step 2 (Automate) → Step 3 (Outcome).
6. **Outcomes Grid (Benefits > Features):** Focus on what the user achieves, not just code specs.
7. **Social Proof & Testimonials:** High-fidelity cards with photo avatars, job titles, and quantifiable wins.
8. **Objection-Led FAQ:** Directly answer the top 6–12 customer doubts and risk fears.
9. **Final Conversion Banner:** Restate the core offer, clear CTA, and zero-risk guarantee.
10. **Minimalist Footer:** Essential legal links, brand copyright, and status badge.

---

### A3. Layout Archetypes
Select one primary layout archetype based on product intent:
- **Layout A (SaaS & Developer Tools):** Split hero (left copy + right product screenshot / interactive mockup), 3-column feature grid, interactive tabbed demo.
- **Layout B (Direct Conversion & Waitlists):** Centered high-impact hero, single email capture input, proof pill, compact one-screen experience.
- **Layout C (High-Ticket & Services):** Narrative editorial layout, deep pain-point exposition, video testimonial embeds, calendar booking integration.
- **Layout D (Multi-Persona Solutions):** Persona toggle tab (e.g. "For Developers" vs "For Founders") dynamically swapping hero benefits and proof points.

---

### A4. Conversion Copywriting Formulas
- **Value Headline:** `[Action Verb] [Desired Outcome] without [Primary Pain Point]`
- **Subheadline:** 1–2 sentences explaining *how* it works and *who* it is for. Maximum line width: `680px`.
- **Action CTA:** Action verb + tangible outcome (`Start Free Trial`, `Build My Agent`, `Claim 14-Day Pass`). Never use `Submit`, `Click Here`, or `Learn More`.
- **Friction Killers:** Place immediately adjacent to CTA: *"No credit card required • 2-minute setup • Cancel anytime"*.
- **Quantified Outcomes:** Always prefer specific metrics over vague promises (*"Cuts build times by 68%"* beats *"Blazing fast builds"*).

---

## PART B — THE VISUAL SYSTEM (DO THIS SECOND)

Every visual style must strictly bind to design tokens rather than ad-hoc inline styles.

### B1. Typography
- **Primary Typefaces:** `Geist`, `Manrope`, `Poppins`, or `Plus Jakarta Sans`.
- **Code & Metric Typefaces:** `Geist Mono` or `JetBrains Mono` strictly for code, metrics, tables, and tags.
- **Banned Typefaces:** `Inter`, `Roboto`, `Arial`, `Open Sans` (avoid generic AI defaults).
- **Rules:**
  - One typeface family per landing page (plus one monospace family for metrics/code).
  - No italic typography anywhere.
  - No ultra-heavy weights (`font-black` / 900); stick to `font-normal` (400), `font-medium` (500), and `font-semibold` (600).
  - Explicit size scale: `12px` (caption), `14px` (sub-body), `16px` (body), `20px` (h4), `28px` (h3), `40px` (h2), `56px–72px` (h1).

### B2. Spacing Tokens
Strict spacing scale only: `0`, `2px`, `4px`, `8px`, `12px`, `16px`, `24px`, `32px`, `40px`, `48px`, `64px`, `80px`, `96px`, `128px`.
Never use arbitrary spacing values like `margin: 19px` or `padding: 37px`.

### B3. Corner Radii & Hierarchy
Follow the concentric rounding rule:
$$R_{outer} = R_{inner} + \text{Padding}$$
- Large containers: `rounded-2xl` (16px) or `rounded-3xl` (24px)
- Cards inside containers: `rounded-xl` (12px)
- Buttons and inputs: `rounded-lg` (8px) or `rounded-full` (for pills)

### B4. Contrast & Backgrounds
- **Dark Mode:** Deep ink/slate canvas (`#090d16` or `#0b0f17`), cards (`#141e33` or `#131b2e`), borders (`rgba(255, 255, 255, 0.08)`).
- **Light Mode:** Warm ivory or soft stone canvas (`#faf9f5` or `#f8fafc`), card elevated white (`#ffffff`), borders (`#e2e8f0`).
- Ensure all text passes WCAG 2.2 AA ($4.5:1$ for body text, $3:1$ for large titles).

### B5. Hero Section Visuals
- Limit headline and subheadline max-width to `680px` for optimal reading scan lines.
- Subtle gradient overlays permitted only on accent badges or hero text headers.
- Product mockups must include realistic window frames, status bars, and authentic domain data.

### B6. Micro-Interactions & Motion
- All interactive elements must provide active tactile feedback (`active:scale-[0.97]` or `active:scale-95`).
- Transitions must be capped between `150ms` and `250ms` with smooth cubic-bezier easing (`cubic-bezier(0.16, 1, 0.3, 1)`).
- Never add endless looping animations that distract from the conversion CTA.

### B7. Anti-Slop Banned Tropes
- **Banned Copy:** *"Elevate your workflow"*, *"Revolutionize your business"*, *"Seamless integration"*, *"Next-generation solution"*, *"Game-changer"*.
- **Banned Placeholders:** *"Lorem Ipsum"*, *"Acme Corp"*, *"John Doe"*, fake round metrics like `99.9% uptime`.
- **Banned Aesthetics:** Random floating blobs, excessive saturated purple gradients, unstyled standard HTML inputs.
