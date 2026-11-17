<div align="left">
  <a href="./README.md" style="padding: 10px; border-bottom: 2px solid transparent; text-decoration: none; color: #8b949e; font-weight: bold;">📖 README</a>
  &nbsp;&nbsp;&nbsp;
  <a href="./SUPPORT.md" style="padding: 10px; border-bottom: 2px solid #58a6ff; text-decoration: none; color: #c9d1d9; font-weight: bold;">📘 SUPPORT / GUIDE</a>
</div>
<br>

# Swarm IDE - Complete User Guide

Welcome to **Swarm IDE**, a privacy-first, fully local autonomous AI software engineering environment. This guide explains how to use the IDE's core features, manage agentic tasks, and customize the underlying AI models.

---

## 1. Getting Started

### Launching the IDE
To start the Swarm IDE, simply run the main Python script from the root of the project:
```bash
python 6_builder_app.py
```
By default, the server will host the UI at `http://127.0.0.1:5000`. Navigate to this URL in your browser.

For Windows users, you can also double-click **`Start-Swarm.bat`** for a one-click automated startup of both the Ollama daemon and the web server.

---

## 2. Core Operating Modes

The IDE operates in distinct modes, dynamically adjusting its routing based on your request:

### A. The "Search" Mode (Agentic & Visual RAG)
Located in the **Search** tab, this is for knowledge retrieval against your codebase and documentation. 
- You can ask questions about your existing code, architecture, or how to implement a specific pattern.
- The system uses **ChromaDB** for semantic text search and **ColPali (Byaldi)** for visual PDF document retrieval.
- Context is validated using a lightweight evaluation agent (Librarian) before generating synthesized answers.

### B. The "Builder" Mode (Autonomous Swarm Engineering)
Located in the **Builder** tab, this is the core autonomous agent loop. When you issue a command (e.g., "Build a high-craft dashboard component"):
1. **Plans:** Re-evaluates your goal and structures a list of acceptance criteria (`<plan>`).
2. **Deploys Specialized Workers:** Leverages `<spawn_worker>` with assigned skills and roles to parallelize research, coding, and testing.
3. **Executes:** Uses the active local model (e.g., Qwen2.5-Coder, DeepSeek-R1) to iteratively write files, patch code, and run sandbox commands.
4. **Tests & Heals:** Automatically executes unit tests. If a test fails, the agent isolates the root cause via `systematic-debugging` and rewrites code until acceptance criteria pass.

### C. "Heretic Mode" (Uncensored Mode)
By toggling the **Heretic Mode** switch in the sidebar:
- The system bypasses all software engineering restrictions and guardrails.
- The default model dynamically swaps to an uncensored model (e.g., `Hermes-3`), disabling moralizing filters.
- Governance logging tracks invocations in `workspace/governance.db`.

---

## 3. UI Features & Skills Toolkit

- **Skills Arsenal Drawer:** Click the **`⚡ Skills Toolkit (83)`** button in the sidebar to browse all 83 installed skills categorized across Interface Engineering, Swarm Coordination, Research, Tools, and Design Themes. Click **"+ Inject"** to instantly paste skill activation tags into your chat input.
- **Session History:** The left sidebar automatically saves your past conversations and agent runs via LocalStorage. Click on any past session to re-hydrate the terminal and view previous reasoning traces.
- **New Chat:** Click **+ New** to clear the active context and start a fresh request, preventing cross-task context pollution.
- **File & PDF Attachments:** Attach images, PDFs, or code files to your prompt using the paperclip icon. Attached PDFs are automatically ingested into the visual RAG pipeline.
- **Governance Modal:** Click the **"🛡️ Governance Log"** button in the sidebar to view real-time metrics on your local sessions, including total sessions, compute time, and security boundaries.

---

## 4. Multi-Agent Worker Archetypes

The Orchestrator can deploy parallel workers with explicit skills and roles:

```xml
<spawn_worker>
  <task>Audit component radii and button press transitions</task>
  <skill>make-interfaces-feel-better</skill>
  <role>Frontend Craftsman</role>
</spawn_worker>
```

| Worker Archetype | Bound Skill | Responsibility |
|---|---|---|
| **Research Scout** | `last30days` | Real-time cross-platform recency research (Reddit, HN, GitHub) from the past 30 days. |
| **Design Architect** | `create-design-md`, `baseline-ui` | Extracts and enforces design tokens, responsive grids, and container queries. |
| **Frontend Craftsman** | `make-interfaces-feel-better` | Applies concentric border radii, optical alignment, layered shadows, and spring transitions. |
| **Accessibility Auditor** | `better-accessibility` | Audits WCAG 2.2 AA contrast ratios, keyboard focus traps, and ARIA regions. |
| **Test Engineer** | `test-driven-development` | Authors failing unit/integration tests before functional code synthesis. |
| **Code Reviewer** | `requesting-code-review`, `better-interface` | Performs 5-axis PR diff reviews (Correctness, Simplicity, Architecture, Security, Performance). |
| **Security Sentinel** | `security-threat-model` | Evaluates trust boundaries, input escaping, and path traversal vectors. |
| **Root-Cause Debugger** | `systematic-debugging` | Isolates bug root causes with minimal reproduction scripts before patching. |

---

## 5. How to Swap and Configure Models

By default, Swarm IDE uses `qwen2.5-coder:latest` or `deepseek-r1:7b` for reasoning and `hermes3:8b` for Heretic mode. All models run locally via Ollama on port 11434.

### A. Swapping the Main Orchestrator Model via UI
Simply select your desired model from the **Model Engine** dropdown in the left sidebar (`Qwen2.5-Coder`, `Llama-3.1`, `DeepSeek-R1`, or `Hermes-3`).

### B. Swapping the Model Defaults in Code
To change the default model in the backend:
1. Open `6_builder_app.py` in your editor.
2. Locate the default model assignment:
```python
model = data.get('model', 'qwen2.5-coder:latest')
```
3. Update `swarm-ide/backend/agents/orchestrator.py`:
```python
DEFAULT_MODEL = "qwen2.5-coder:latest"
```

### C. Swapping Specialized Sub-Agents
The IDE uses specialized smaller models for specific tasks to conserve GPU memory:
- **Tester Agent** (`swarm-ide/backend/agents/tester.py`):
```python
def diagnose_and_fix(..., model="qwen2.5-coder:7b"):
```
- **Librarian Agent** (`swarm-ide/backend/agents/librarian.py`):
```python
def evaluate_context(..., model="qwen2.5:1.5b"):
```

---

## 6. Real-Time Research with `last30days`

To conduct zero-config real-time research across public platforms from the past 30 days:

### Direct CLI Execution
```bash
python workspace/skills/last30days.py "ai agent breakthroughs" --quick
```

### Agentic Swarm Execution
```xml
<use_skill>
  <name>last30days.py</name>
  <args>"quantum computing breakthroughs" --lookback-days 30</args>
</use_skill>
```

---

## 7. Cinematic Video Rendering (Brag Skill)

To generate launch trailers or UI demos using the Hyperframes engine:
```xml
<render_hyperframes_video>
  <composition_html><![CDATA[... valid GSAP HTML ...]]></composition_html>
  <output_filename>launch_trailer.mp4</output_filename>
</render_hyperframes_video>
```
The sandbox lints the HTML with `npx hyperframes check`, renders the 4K MP4 with headless Chromium and FFmpeg, and moves the finished video into `workspace/`.
