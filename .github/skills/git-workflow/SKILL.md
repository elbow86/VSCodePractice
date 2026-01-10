---
name: git-workflow
description: Guide for Git workflows including branching, committing with conventional commit messages, pull requests, and repository management. Use for Git operations and version control tasks.
---

# Git Workflow

Comprehensive guide for Git operations, branching strategies, and version control best practices.

## Conventional Commits

Always use conventional commit format for clear, parseable commit history.

### Format
```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Types
- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting, semicolons)
- **refactor**: Code restructuring without behavior change
- **perf**: Performance improvements
- **test**: Adding or updating tests
- **build**: Build system or dependency changes
- **ci**: CI/CD pipeline changes
- **chore**: Maintenance tasks

### Examples
```bash
# Feature
git commit -m "feat(auth): add OAuth2 authentication"

# Bug fix
git commit -m "fix(api): resolve null pointer in user endpoint"

# Documentation
git commit -m "docs(readme): update installation instructions"

# Refactoring
git commit -m "refactor(state-machine): apply State design pattern to traffic light"
```

## Branching Strategy

### Branch Naming Convention
```
<type>/<short-description>

# Examples:
feature/user-authentication
fix/payment-bug
refactor/database-layer
docs/api-documentation
```

### Common Workflows

**Feature Development:**
```bash
# Create feature branch
git checkout -b feature/new-feature

# Make changes and commit
git add .
git commit -m "feat(module): add new feature"

# Push to remote
git push -u origin feature/new-feature

# Create PR when ready
```

**Bug Fix:**
```bash
# Create fix branch
git checkout -b fix/bug-description

# Fix and commit
git add .
git commit -m "fix(component): resolve bug description"

# Push and create PR
git push -u origin fix/bug-description
```

## Commit Best Practices

### 1. Atomic Commits
Each commit should be a single logical change:
```bash
# ❌ BAD: Multiple unrelated changes
git commit -m "fix bug and add feature and update docs"

# ✅ GOOD: Separate commits
git commit -m "fix(api): resolve timeout issue"
git add new-feature.py
git commit -m "feat(api): add rate limiting"
git add README.md
git commit -m "docs: document rate limiting feature"
```

### 2. Stage Changes Selectively
```bash
# Stage specific files
git add file1.py file2.py

# Stage parts of files interactively
git add -p file.py

# Review staged changes
git diff --staged
```

### 3. Review Before Commit
```bash
# Check status
git status

# Review changes
git diff

# Review staged changes
git diff --staged

# Then commit
git commit -m "type(scope): description"
```

## Pull Request Workflow

### Creating a PR

**1. Ensure branch is up to date:**
```bash
# Update main branch
git checkout main
git pull origin main

# Rebase your feature branch
git checkout feature/your-feature
git rebase main
```

**2. Push your branch:**
```bash
git push origin feature/your-feature
```

**3. Create PR with clear description:**
```markdown
## Description
Brief summary of changes

## Changes Made
- Change 1
- Change 2
- Change 3

## Testing
- [ ] Unit tests pass
- [ ] Manual testing completed
- [ ] No breaking changes

## Related Issues
Closes #123
```

### Reviewing PRs

**For reviewers:**
1. Check code quality and style
2. Verify tests are included
3. Test functionality locally if needed
4. Provide constructive feedback
5. Approve when satisfied

**For authors:**
1. Address all review comments
2. Make requested changes in new commits
3. Respond to questions
4. Request re-review when ready

## Common Git Operations

### Undoing Changes

```bash
# Undo uncommitted changes to a file
git checkout -- file.py

# Unstage a file
git reset HEAD file.py

# Amend last commit (not pushed)
git commit --amend -m "new message"

# Revert a commit (creates new commit)
git revert <commit-hash>

# Reset to previous commit (dangerous if pushed)
git reset --hard HEAD~1
```

### Branch Management

```bash
# List branches
git branch -a

# Switch branches
git checkout branch-name

# Create and switch to new branch
git checkout -b new-branch

# Delete local branch
git branch -d branch-name

# Delete remote branch
git push origin --delete branch-name

# Rename current branch
git branch -m new-name
```

### Stashing Changes

```bash
# Stash uncommitted changes
git stash

# Stash with message
git stash save "WIP: feature description"

# List stashes
git stash list

# Apply most recent stash
git stash apply

# Apply and remove stash
git stash pop

# Apply specific stash
git stash apply stash@{2}

# Clear all stashes
git stash clear
```

### Viewing History

```bash
# View commit log
git log

# Compact log
git log --oneline

# Show changes in each commit
git log -p

# Show last N commits
git log -n 5

# View changes to a file
git log -p -- file.py

# Search commits
git log --grep="keyword"
```

## Resolving Conflicts

```bash
# When conflicts occur during merge/rebase
git status  # See conflicted files

# Edit files to resolve conflicts
# Look for <<<<<<, =======, >>>>>> markers

# After resolving, stage files
git add resolved-file.py

# Continue merge/rebase
git rebase --continue  # for rebase
# or
git commit  # for merge
```

## Git Configuration

### User Setup
```bash
# Set name and email
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Set default editor
git config --global core.editor "code --wait"

# Set default branch name
git config --global init.defaultBranch main
```

### Useful Aliases
```bash
# Create shortcuts
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.cm commit
git config --global alias.lg "log --oneline --graph --decorate"

# Use with: git st, git co, etc.
```

## Best Practices Summary

1. **Commit Often**: Small, frequent commits are better than large ones
2. **Write Clear Messages**: Use conventional commit format
3. **Pull Before Push**: Always sync with remote before pushing
4. **Review Changes**: Use `git diff` before committing
5. **Test Before Commit**: Ensure tests pass
6. **Rebase, Don't Merge**: Keep history clean with rebase
7. **Never Force Push**: Unless you're absolutely sure and it's your branch
8. **Use Branches**: One branch per feature or fix
9. **Delete Merged Branches**: Keep repository clean
10. **Commit Complete Work**: Don't commit broken code
