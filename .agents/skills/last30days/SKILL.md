---
name: last30days
description: Researches any topic, framework, product, or news across Reddit, X (Twitter), YouTube, Hacker News, Polymarket, and GitHub strictly within the past 30 days, scoring by real community engagement (upvotes, comments, market volume) rather than SEO.
---

# `last30days` Research Engine

The `last30days` skill turns an AI agent or swarm into a real-time intelligence engine. Instead of relying on static training data or SEO-manipulated search engine results, it aggregates public discussions, developer reactions, social sentiment, and prediction market odds strictly from the **past 30 days**.

## Core Capabilities
- **Multi-Source Aggregation**: Queries Reddit, Hacker News, Polymarket, GitHub repositories/issues, YouTube, and X.
- **Engagement-Scored Weighting**: Ranks insights by organic community validation (upvotes, reaction counts, comment depth, betting volume) rather than marketing copy.
- **Recency Filter**: Strictly ignores stale blog posts, outdated documentation, and historic discussions older than 30 days.

## When to Use
- User asks about recent events, releases, or trending tech: "What are people saying about Python 3.13?", "What are the latest developments in AI agents?", "How is the community reacting to the new Next.js release?".
- Market sentiment or prediction queries: "What are the odds on Polymarket for...".
- Validating whether a bug, library deprecation, or breaking change emerged recently.

## How to Run

### In the Swarm IDE
Execute via the native Python skill runner:
```xml
<use_skill>
  <name>last30days.py</name>
  <args>"quantum computing breakthroughs" --quick</args>
</use_skill>
```

Or run via CLI:
```bash
python workspace/skills/last30days.py "topic to research" --emit=compact
```

### CLI Options:
- `topic`: The query, entity, or product name.
- `--quick`: Faster retrieval pass across primary sources.
- `--lookback-days [N]`: Temporal boundary in days (default: 30).
- `--preflight`: Verify source connectivity and configuration without running search.
- `--emit [compact|json|full]`: Output format (default: compact).

## Output Synthesis Guidelines
When presenting findings gathered from `last30days`:
1. **Anchor with Dates**: Explicitly note timestamps and relative dates (e.g., "5 days ago on Reddit r/LocalLLaMA...").
2. **Highlight Engagement**: Mention upvotes, star surges, or comment volume to indicate signal strength.
3. **Cluster Perspectives**: Separate developer consensus, skepticism/controversy, and quantitative predictions.
4. **Cite Exact URLs**: Always provide the direct source links gathered by the engine.
