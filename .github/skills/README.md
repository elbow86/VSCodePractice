# Agent Skills for VS Code

This directory contains **Agent Skills** - folders of instructions that teach Claude and other AI assistants how to perform specialized tasks. Skills are part of the [Agent Skills open standard](https://agentskills.io) supported by VS Code 1.109 Insiders and later.

## What are Agent Skills?

Agent Skills are folders containing a `SKILL.md` file with YAML frontmatter and markdown instructions. They give AI agents:

- **Domain expertise** - Specialized knowledge for specific tasks
- **Repeatable workflows** - Consistent, auditable processes
- **New capabilities** - Enhanced abilities for complex operations
- **Context** - Company, team, or user-specific information

## Available Skills

### 1. **python-test-runner** (`python-test-runner/`)
Run Python tests with pytest, analyze results, and provide coverage reports.

**Use when:** Running tests, checking coverage, verifying Python code functionality

### 2. **code-reviewer** (`code-reviewer/`)
Comprehensive code review analyzing security, performance, maintainability, and design patterns.

**Use when:** Reviewing code changes, pull requests, or providing quality feedback

### 3. **git-workflow** (`git-workflow/`)
Git operations with conventional commits, branching strategies, and best practices.

**Use when:** Managing Git operations, creating commits, or handling version control

## Using Skills in VS Code

Skills are automatically discovered by VS Code when placed in `.github/skills/`. Each skill folder contains:

```
skill-name/
├── SKILL.md          # Main skill definition (required)
├── scripts/          # Optional helper scripts
├── reference/        # Optional reference documentation
└── examples/         # Optional example files
```

### Skill Structure (SKILL.md)

```markdown
---
name: skill-name
description: Clear description of what this skill does and when to use it
---

# Skill Name

[Instructions that the AI will follow when this skill is active]

## When to Use This Skill

[Describe scenarios where this skill should be invoked]

## Process/Workflow

[Step-by-step instructions]

## Best Practices

[Guidelines for using this skill effectively]
```

### Invoking Skills

In VS Code chat, reference skills naturally:
```
Use the code reviewer skill to analyze this function
```

```
Run the Python tests using the test runner skill
```

Claude and compatible agents automatically detect and use relevant skills based on the task context.

## Creating Custom Skills

1. **Create skill folder:**
   ```
   .github/skills/your-skill-name/
   ```

2. **Add SKILL.md with frontmatter:**
   ```markdown
   ---
   name: your-skill-name
   description: What this skill does and when to use it
   ---
   
   # Your Skill Name
   
   [Instructions go here]
   ```

3. **Add supporting resources (optional):**
   - `scripts/` - Executable helper scripts
   - `reference/` - Documentation to reference
   - `examples/` - Example usage files

4. **Reload VS Code window** to register the new skill

## Skill Design Best Practices

### ✅ Do:
- Write clear, specific instructions
- Include concrete examples
- Specify when to use the skill
- Provide decision trees for complex workflows
- Include error handling guidance
- Reference external documentation when needed

### ❌ Don't:
- Make instructions too vague or general
- Assume context the AI won't have
- Create overly long instructions (break into sections)
- Forget to specify file paths or commands explicitly

## Example Skill Patterns

### Simple Skill (Task Instructions)
```markdown
---
name: simple-task
description: Perform a specific task with clear steps
---

# Simple Task

Follow these steps:
1. Check preconditions
2. Execute main operation
3. Verify results
```

### Complex Skill (Decision Tree)
```markdown
---
name: complex-workflow
description: Handle complex scenarios with branching logic
---

# Complex Workflow

## Decision Tree

User task → Is condition A met?
    ├─ Yes → Do action 1
    └─ No → Is condition B met?
        ├─ Yes → Do action 2
        └─ No → Do action 3
```

### Skill with Scripts
```markdown
---
name: automated-task
description: Use helper scripts for complex automation
---

# Automated Task

Use the helper script in `scripts/`:

```bash
python scripts/helper.py --option value
```

Script handles [specific complexity].
```

## Resources

- **Official Specification:** [agentskills.io/specification](https://agentskills.io/specification)
- **Example Skills:** [github.com/anthropics/skills](https://github.com/anthropics/skills)
- **VS Code Support:** [code.visualstudio.com](https://code.visualstudio.com/)
- **Agent Skills Ecosystem:** [agentskills.io](https://agentskills.io)

## Compatible AI Assistants

Agent Skills are supported by:
- Claude (Claude.ai, Claude Code, API)
- VS Code with GitHub Copilot
- Cursor
- Goose
- And other skills-compatible tools

---

*Agent Skills is an open standard developed by Anthropic and adopted by the AI tooling ecosystem. Learn more at [agentskills.io](https://agentskills.io).*
