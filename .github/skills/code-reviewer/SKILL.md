---
name: code-reviewer
description: Perform comprehensive code reviews analyzing security, performance, maintainability, and best practices. Use when reviewing code changes, pull requests, or providing code quality feedback.
---

# Code Reviewer

Conduct thorough code reviews with focus on security, performance, design patterns, and maintainability.

## Review Process

### 1. Initial Assessment

Start by understanding the code's context:
- **Purpose**: What is this code trying to accomplish?
- **Scope**: How much code is being reviewed?
- **Language**: What language and frameworks are used?
- **Dependencies**: What external libraries are involved?

### 2. Security Analysis

Check for common security vulnerabilities:

**Input Validation:**
- Are user inputs properly validated and sanitized?
- Is there protection against injection attacks (SQL, XSS, command)?
- Are file paths validated to prevent directory traversal?

**Authentication & Authorization:**
- Are credentials properly protected (no hardcoded secrets)?
- Is authentication properly implemented?
- Are authorization checks in place where needed?

**Data Protection:**
- Is sensitive data encrypted in transit and at rest?
- Are passwords properly hashed (bcrypt, argon2)?
- Is PII (Personal Identifiable Information) handled correctly?

**Common Vulnerabilities:**
```python
# ❌ BAD: SQL injection risk
query = f"SELECT * FROM users WHERE id = {user_id}"

# ✅ GOOD: Parameterized query
query = "SELECT * FROM users WHERE id = ?"
cursor.execute(query, (user_id,))
```

### 3. Performance Review

Identify performance issues:

**Algorithm Efficiency:**
- Are there O(n²) loops that could be O(n)?
- Are there redundant database queries?
- Could operations be batched?

**Resource Management:**
- Are files/connections properly closed?
- Are large datasets loaded into memory unnecessarily?
- Are there memory leaks?

**Caching Opportunities:**
- Could results be cached?
- Are expensive operations repeated unnecessarily?

Example issues:
```python
# ❌ BAD: N+1 query problem
for user in users:
    orders = db.query(f"SELECT * FROM orders WHERE user_id = {user.id}")

# ✅ GOOD: Single query with join
orders = db.query("SELECT * FROM orders WHERE user_id IN (?)", user_ids)
```

### 4. Code Quality Assessment

**Readability:**
- Are variable names descriptive?
- Is the code well-organized?
- Is there appropriate commenting?
- Are functions/methods reasonably sized?

**Maintainability:**
- Is the code DRY (Don't Repeat Yourself)?
- Are magic numbers avoided?
- Is error handling comprehensive?
- Is the code testable?

**Design Patterns:**
- Are appropriate design patterns used?
- Is there separation of concerns?
- Is coupling minimized?
- Is cohesion maximized?

### 5. Best Practices Check

**Language-Specific:**
- Python: PEP 8 compliance, type hints, context managers
- JavaScript: ESLint rules, modern syntax (ES6+)
- TypeScript: Proper type annotations, avoiding `any`
- Java: Following Java conventions, proper exception handling

**Testing:**
- Are there unit tests?
- Is test coverage adequate?
- Are edge cases covered?
- Are tests meaningful (not just for coverage)?

**Documentation:**
- Are public APIs documented?
- Are complex algorithms explained?
- Is there a README for the module?
- Are deprecations noted?

## Review Output Format

Provide structured feedback:

### 🔴 Critical Issues (Must Fix)
- Security vulnerabilities
- Data loss risks
- Major performance problems

### 🟡 Important Issues (Should Fix)
- Code smells
- Maintainability concerns
- Missing error handling

### 🟢 Suggestions (Nice to Have)
- Refactoring opportunities
- Better naming
- Additional documentation

### ✅ Positive Feedback
- Well-implemented patterns
- Good test coverage
- Clear documentation

## Example Review

```markdown
## Review of user_service.py

### 🔴 Critical Issues

1. **SQL Injection Vulnerability (Line 45)**
   ```python
   # Current code
   query = f"SELECT * FROM users WHERE email = '{email}'"
   
   # Recommended fix
   query = "SELECT * FROM users WHERE email = ?"
   cursor.execute(query, (email,))
   ```

### 🟡 Important Issues

2. **Missing Error Handling (Line 67)**
   The database connection should be wrapped in try-except

3. **N+1 Query Problem (Line 89-93)**
   Loading user preferences in a loop causes multiple queries

### 🟢 Suggestions

4. **Consider Type Hints (Throughout)**
   Adding type hints would improve code clarity

### ✅ Positive Feedback

- Excellent test coverage (95%)
- Clear function naming
- Good separation of concerns
```

## Design Pattern Recognition

Identify opportunities for common patterns:

**Creational Patterns:**
- Factory, Builder, Singleton

**Structural Patterns:**
- Adapter, Decorator, Facade

**Behavioral Patterns:**
- Strategy, Observer, Command, State

Example:
```python
# Opportunity for Strategy Pattern
if payment_type == "credit_card":
    # credit card logic
elif payment_type == "paypal":
    # paypal logic
elif payment_type == "crypto":
    # crypto logic

# Better: Use Strategy Pattern
payment_processor = PaymentProcessorFactory.create(payment_type)
payment_processor.process(amount)
```

## Review Checklist

- [ ] Security vulnerabilities identified
- [ ] Performance issues noted
- [ ] Code smells highlighted
- [ ] Design pattern opportunities suggested
- [ ] Best practices violations flagged
- [ ] Positive aspects acknowledged
- [ ] Actionable recommendations provided
- [ ] Priority levels assigned
