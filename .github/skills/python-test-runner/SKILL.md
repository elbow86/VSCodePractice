---
name: python-test-runner
description: Run Python tests with pytest and analyze results. Use when the user asks to run tests, check test coverage, or verify Python code functionality.
---

# Python Test Runner

Run Python tests using pytest with comprehensive output and analysis.

## When to Use This Skill

Use this skill when you need to:
- Run unit tests for Python code
- Verify code functionality after changes
- Check test coverage
- Identify failing tests and their causes
- Run specific test files or test cases

## Test Execution Process

### 1. Check for Test Files

First, identify test files in the project:
```bash
# Look for test files
Get-ChildItem -Recurse -Filter "test_*.py"
Get-ChildItem -Recurse -Filter "*_test.py"
```

### 2. Run Tests with Pytest

Execute tests with verbose output:
```bash
# Run all tests
pytest -v

# Run specific test file
pytest path/to/test_file.py -v

# Run specific test function
pytest path/to/test_file.py::test_function_name -v

# Run with coverage report
pytest --cov=. --cov-report=term-missing -v
```

### 3. Analyze Test Results

Review the output for:
- **Passed tests** - Verify expected functionality works
- **Failed tests** - Identify what broke and why
- **Error details** - Read tracebacks and assertion messages
- **Coverage gaps** - Identify untested code paths

## Common Test Patterns

### Running Tests After Code Changes
```bash
# Run tests related to changed files
pytest -v path/to/modified_module/

# Run tests with immediate failure stopping
pytest -x -v
```

### Debugging Failed Tests
```bash
# Show local variables on failure
pytest -v --showlocals

# Enter debugger on failure
pytest -v --pdb
```

### Test Selection
```bash
# Run tests by keyword
pytest -v -k "test_user"

# Run tests by marker
pytest -v -m "slow"
```

## Best Practices

1. **Always activate virtual environment** before running tests
2. **Review test output carefully** - don't just check pass/fail
3. **Run tests after any code modification** to catch regressions
4. **Use coverage reports** to identify untested code
5. **Fix failing tests immediately** - don't let them accumulate

## Example Workflow

```python
# 1. User makes code changes
# 2. You run: pytest -v
# 3. Analyze results and report to user
# 4. If tests fail, help debug by:
#    - Reading the traceback
#    - Identifying the problem
#    - Suggesting fixes
```

## Integration with Development

This skill integrates well with:
- Code refactoring workflows
- Bug fixing processes
- Feature development
- Code review procedures
