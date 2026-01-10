# Agent Memory (Auto-Synced)

This file is the centralized, version-controlled view of agent memory.

- Source of truth: the individual files under `/memories` (managed by the agent-memory extension).
- Sync: when `agentMemory.autoSyncToFile` is configured, the extension automatically updates this file.

Last synced: 2026-01-09

---

## State machine UI visualizers
- Added Tkinter-based state visualizers under `StateMachine-Expt/ui/`.
- Shared widget: `StateMachine-Expt/ui/tk_state_graph.py` (draws directed state graph, highlights active state).
- Apps:
  - `StateMachine-Expt/ui/traffic_light_visualizer.py` (steps through `SimpleTrafficLight`)
  - `StateMachine-Expt/ui/vending_machine_visualizer.py` (drives `VendingMachine` actions)
- Documentation: updated `StateMachine-Expt/STATE_PATTERN_README.md` with run commands.

## VSCodePractice – Project Context

### Context
- Workspace/repo: `elbow86/VSCodePractice` (branch: `master`, default: `master`)
- Purpose: Practice workspace for learning VS Code development workflows and patterns

### Agent-Memory Auto-Sync (Corrected 2026-01-09)
- Agent Memory extension auto-syncs to `.github/copilot/memory.instructions.md`
- Setting location: `.vscode/settings.json`
- Previously incorrectly documented as `AGENTS.md`; corrected on 2026-01-09
- Note: Reload VS Code window if sync doesn't occur immediately

### Python Virtual Environment
- Virtual environment located at `.venv/`
- Activation script: `.venv/Scripts/Activate.ps1` (PowerShell)
- Used for project dependencies

### Decisions Made
- **2025-12-18**: Enabled agent-memory file auto-sync
- **2026-01-07**: Added repo-root `.gitignore` with standard Python ignores (including `__pycache__/` and `*.py[cod]`)
- **2026-01-07**: Untracked committed `__pycache__` directories from git index
- **2026-01-09**: Corrected auto-sync target to `.github/copilot/memory.instructions.md`

### Learnings

#### Python / Git Hygiene (2026-01-07)
- `__pycache__/` and `*.pyc` should not be committed (generated artifacts, vary by interpreter/version)
- Fix accidentally committed caches:
  - Add root `.gitignore` rule (`__pycache__/`, `*.py[cod]`)
  - Untrack with `git rm -r --cached <path>` (keeps local files)

#### Agent Memory Extension
- Can consolidate all individual entries under `/memories` into one workspace file when `agentMemory.autoSyncToFile` is set
- Memory store path `/memories` initially returned "Path not found" when no persisted memory entries existed

### User Preferences
- **2026-01-07**: Every new project should start with appropriate `.gitignore` (at least Python + OS/editor + venv ignores)

### Next Steps
- Maintain `.github/copilot/memory.instructions.md` as central, version-controlled memory view (auto-synced from `/memories`)
- Add future durable notes: architecture decisions, conventions, recurring commands, environment setup
- Consider committing `.gitignore` and cached deletions

### Pitfalls Avoided
- Prevented ongoing noisy diffs by removing tracked bytecode caches and adding ignores
- Avoided deleting local cache files (used `--cached` flag)
- Avoided duplicating memory entries by checking `/memories` first
