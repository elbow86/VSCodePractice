# Copilot Instructions

This file provides guidance for AI coding agents working in this codebase.

## Project Overview

This is a practice workspace for learning VS Code development workflows and patterns.

## Architecture & Structure

- **Root Directory**: Contains configuration files and main project structure
- **Development Setup**: Standard Node.js/Python/etc. project (to be determined based on project type)
- **Design Patterns**: Modular code organization, separation of concerns
Identify and consider Design Patterns as in the 1995 Gang of Four book

## Development Workflows

### Getting Started
```bash
# Clone and setup
git clone <repository-url>
cd VSCodePractice

# Install dependencies (adjust based on project type)
npm install
# or
pip install -r requirements.txt
```

### Build & Run
```bash
# Development server
npm start
# or
python main.py

# Build for production
npm run build
```

### Testing
```bash
# Run tests
npm test
# or
pytest
```

## Coding Conventions

### File Organization
- Use descriptive file and folder names
- Group related functionality together
- Separate configuration from source code

### Code Style
- Follow language-specific best practices
- Use meaningful variable and function names
- Include comments for complex logic
- Maintain consistent formatting

### Git Workflow
- Use descriptive commit messages
- Create feature branches for new work
- Keep commits focused and atomic

## Key Files & Patterns

- `README.md` - Project documentation and setup instructions
- `.gitignore` - Version control exclusions
- Package configuration files (`package.json`, `requirements.txt`, etc.)

## External Dependencies

- Document any external services or APIs
- Include authentication setup if needed
- Note environment variable requirements

## Debugging & Troubleshooting

### Common Issues
- Check dependency installation
- Verify environment variables
- Review error logs in terminal

### VS Code Setup
- Use workspace settings for consistent configuration
- Install recommended extensions
- Configure debug launch configurations as needed

---

*This file should be updated as the project evolves and new patterns emerge.*