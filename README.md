<div align="left">
  <a href="./README.md" style="padding: 10px; border-bottom: 2px solid #58a6ff; text-decoration: none; color: #c9d1d9; font-weight: bold;">📖 README</a>
  &nbsp;&nbsp;&nbsp;
  <a href="./SUPPORT.md" style="padding: 10px; border-bottom: 2px solid transparent; text-decoration: none; color: #8b949e; font-weight: bold;">📘 SUPPORT / GUIDE</a>
</div>
<br>

<p align="center">
  <img src="https://img.shields.io/badge/Local-100%25_Offline-000000?style=for-the-badge&logo=git" alt="Offline">
  <img src="https://img.shields.io/badge/Ollama-Local_Models-blue?style=for-the-badge&logo=ollama" alt="Ollama">
  <img src="https://img.shields.io/badge/Skills-83_Installed-purple?style=for-the-badge" alt="83 Skills">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License">
</p>

# Swarm IDE

**An air-gapped, auto-healing autonomous multi-agent developer environment.** Swarm IDE runs completely offline on your local hardware using Ollama. When tasks are dispatched, an autonomous Orchestrator deploys specialized sub-agents armed with portable skills (from [AgenticSkills.io](https://agenticskills.io/)), self-heals failing code through an isolated sandbox, audits interfaces against world-class design standards, and produces production-grade software—with zero cloud dependencies.

---

## 🧠 System Architecture

The Swarm IDE architecture is organized into decoupled layers:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        Swarm IDE Web Interface                        │
│    (React, Tailwind, Skills Arsenal Drawer, Worker Grid, Governance)   │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ HTTP / SSE Stream
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│               Waitress WSGI Server (6_builder_app.py)                  │
│       - Session Management        - AST Pre-Linting (py_compile)       │
│       - REST APIs (/api/skills)   - Dynamic Prompt Compiler            │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│              Autonomous Swarm Loop (builder_loop.py)                   │
│  ┌───────────────────────┐          ┌───────────────────────────────┐  │
│  │   Swarm Orchestrator  │ ───────► │ Parallel Worker Sub-Agents    │  │
│  │ (Qwen2.5 / DeepSeek)  │          │ (Thread-pool with Skills)     │  │
│  └───────────────────────┘          └───────────────────────────────┘  │
│            ▲                                      │                    │
│            └──────────────────────────────────────┘                    │
└───────┬───────────────────────────┬────────────────────────────┬───────┘
        │                           │                            │
        ▼                           ▼                            ▼
┌─────────────────┐       ┌────────────────────┐       ┌─────────────────┐
│ Skills Arsenal  │       │ Dual-Index RAG     │       │ Safe Execution  │
│ (83 Frameworks  │       │ - ColPali (Visual) │       │ Sandbox         │
│  & Python Tools)│       │ - ChromaDB (Text)  │       │ (Docker/Subproc)│
└─────────────────┘       └────────────────────┘       └─────────────────┘
```

### 1. Dynamic Swarm Orchestrator
The central coordinator managing execution state across an iterative XML action loop. The Orchestrator plans tasks, breaks them down into discrete sub-goals, and delegates parallel work to specialized sub-agents using `<spawn_worker>` rather than writing all code in a single prompt.

### 2. Role-Based Worker Specialization
Workers are not generic text prompt wrappers. When the Orchestrator calls `<spawn_worker>`, it assigns an explicit **Role** and an installed **Skill Framework**. The runtime dynamically injects the skill's instructions into the sub-agent's prompt, guaranteeing domain-specific rigor (such as TDD tests, optical alignment, or WCAG contrast compliance).

### 3. Dual-Index Visual & Textual RAG
- **Visual PDF Retrieval (ColPali / Byaldi)**: Ingests attached PDFs using multi-vector vision models (ColPali-v1.2) to understand diagrams, architectural blueprints, tables, and complex layout semantics without lossy OCR.
- **Semantic Codebase Retrieval (ChromaDB)**: Embeds source code files using local sentence-transformers, verified by an autonomous Librarian agent before context injection.

### 4. Self-Healing & Root-Cause Isolation
When tests fail or scripts crash, the Swarm rejects blind trial-and-error edits. A specialized Tester agent enforces `systematic-debugging`: reproducing the bug with a minimal test case, isolating the root cause, and executing a verified regression fix.

### 5. Production WSGI Backend
The server runs on Waitress bound to `127.0.0.1:5000` with strict threading locks to prevent Local LLM Out-Of-Memory (OOM) deadlocks on consumer GPUs.

---

## ⚡ 83-Skill Arsenal (AgenticSkills.io)

Swarm IDE comes pre-loaded with **83 portable agent frameworks and tools** following the open `SKILL.md` standard:

### A. Interface & UI Engineering
| Skill | Source | Primary Responsibility |
|---|---|---|
| **`make-interfaces-feel-better`** | Jakub Krehel | Concentric border radii ($R_{outer} = R_{inner} + \text{padding}$), optical alignment over bounding boxes, layered diffuse shadows, `scale(0.96)` active states, tabular numbers, and spring physics transitions (150ms–250ms). |
| **`better-interface`** | Jakub Krehel | 6-domain interface audit orchestrator (layout hierarchy, typography tracking, semantic color tokens, WCAG compliance, microcopy, component state machines). |
| **`baseline-ui`** | ibelick | Modern frontend constraints, mobile-first responsive container queries, and a 300ms duration cap to prevent sluggish animations. |
| **`create-design-md`** | ibelick | Automates extraction of design tokens, font scales, and component invariants into a unified project `DESIGN.md`. |
| **`better-accessibility`** | a11y Standards | Enforces WCAG 2.2 AA/AAA compliance ($\ge 4.5:1$ contrast, keyboard focus traps, visible focus rings, ARIA live regions). |

### B. Swarm Multi-Agent Coordination & QA
| Skill | Source | Primary Responsibility |
|---|---|---|
| **`requesting-code-review`** | obra / Addy Osmani | Standardizes 5-axis review handoff contracts between workers and reviewer subagents to preserve context window limits. |
| **`systematic-debugging`** | Trail of Bits | Prohibits shotgun debugging. Enforces a 4-step pipeline: Reproduce $\rightarrow$ Isolate $\rightarrow$ Hypothesize $\rightarrow$ Verify. |
| **`test-driven-development`** | Agentic Standard | Enforces the strict Red-Green-Refactor cycle for spawned workers. |
| **`security-threat-model`** | OWASP / Trail of Bits | STRIDE-based attack surface auditing (trust boundaries, input validation, path traversal, and secret leakage prevention). |

### C. Real-Time Research Engine
| Skill | Source | Primary Responsibility |
|---|---|---|
| **`last30days`** | mvanhorn | Stdlib-only Python engine searching Reddit, Hacker News, Polymarket, and GitHub strictly within the past 30 days, scored by organic community engagement rather than SEO. |

### D. Design Themes & Aesthetic Frameworks (70+ Pre-Installed)
Includes *Taste Skill*, *Impeccable*, *Bento*, *Shadcn*, *Neobrutalism*, *Glassmorphism*, *Claude*, *Editorial*, *Minimal*, *Claymorphism*, *Matrix*, *Terracotta*, and the entire Awesome Design library.

---

## 🤖 The 8 Specialized Worker Archetypes

The Orchestrator deploys workers using structured XML tags:

```xml
<spawn_worker>
  <task>Design a responsive analytics card with micro-interactions</task>
  <skill>make-interfaces-feel-better</skill>
  <role>Frontend Craftsman</role>
</spawn_worker>
```

1. **Research Scout** (`last30days`): Real-time recency research before planning.
2. **Design Architect** (`create-design-md` / `baseline-ui`): Establishes tokens and container layout invariants.
3. **Frontend Craftsman** (`make-interfaces-feel-better`): Applies concentric radii, optical alignment, layered shadows, scale(0.96) press feedback, and spring physics.
4. **Accessibility Auditor** (`better-accessibility`): Audits WCAG AA contrast, keyboard navigation, and ARIA patterns.
5. **Test Engineer** (`test-driven-development`): Authors failing tests before functional code synthesis.
6. **Code Reviewer** (`requesting-code-review` / `better-interface`): Evaluates diffs across correctness, simplicity, architecture, security, and performance.
7. **Security Sentinel** (`security-threat-model`): Audits trust boundaries, sanitization, and attack surfaces.
8. **Root-Cause Debugger** (`systematic-debugging`): Isolates bug root causes before applying patches.

---

## 🎬 Cinematic Video Rendering (Brag Skill)

Swarm IDE natively integrates the Hyperframes deterministic rendering tool:

```xml
<render_hyperframes_video>
  <composition_html><![CDATA[... valid GSAP HTML ...]]></composition_html>
  <output_filename>launch_trailer.mp4</output_filename>
</render_hyperframes_video>
```
The backend automatically executes `npx hyperframes check`, renders the 4K MP4 with headless Chromium and FFmpeg, and moves the finished video into `workspace/`.

---

## 🌐 REST API Reference

The backend exposes REST endpoints for IDE integration:

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Serves the single-page React Swarm IDE interface. |
| `POST` | `/build` | Initiates the autonomous multi-agent builder loop (SSE stream). |
| `POST` | `/search` | Queries the Living RAG vector store. |
| `GET` | `/api/skills` | Lists all 83 installed skills with categories and descriptions. |
| `GET` | `/api/skills/<slug>` | Returns the full `SKILL.md` or script content for interactive preview. |
| `GET` | `/governance_stats` | Returns real-time session audit logs, token burn, and safety metrics. |

---

## 🚀 Quick Start

### 1. Requirements
- Python 3.10+
- [Ollama](https://ollama.com) installed and running locally
- Recommended GPU: 8GB+ VRAM (NVIDIA RTX 3060/4060 or Apple Silicon M-series)

### 2. Grab the Recommended Models
```bash
ollama pull qwen2.5-coder:latest
ollama pull deepseek-r1:7b
ollama pull hermes3:8b
```

### 3. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 4. Boot the Swarm Environment
* **Windows (One-Click)**: Double-click **`Start-Swarm.bat`**.
* **CLI Startup**:
```bash
ollama serve &
python 6_builder_app.py
```
Open your browser to `http://127.0.0.1:5000`.

---

## 📄 License

This project is licensed under the **MIT License**. Free for personal and commercial use.
