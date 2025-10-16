# Documentation Prompts

## README Generation

```
Create a comprehensive README.md for this project.

**Project Details:**
- Name: [Project name]
- Purpose: [What the project does]
- Target audience: [Who would use this]
- Technology stack: [Languages, frameworks, tools]

**Include sections for:**
- Project description and features
- Installation instructions
- Usage examples
- Configuration options
- API documentation (if applicable)
- Contributing guidelines
- License information

**Tone:** [Professional/Casual/Technical]
**Existing documentation to reference:** [List any existing docs]
```

## API Documentation

```
Generate API documentation for [ENDPOINT/MODULE].

**Details:**
- Base URL: [API base URL]
- Authentication: [Auth method]
- Data format: [JSON/XML/etc.]

**Endpoints to document:**
[List endpoints or paste code]

**Include for each endpoint:**
- HTTP method and path
- Description and purpose
- Parameters (query, path, body)
- Request/response examples
- Error codes and messages
- Rate limiting (if applicable)

**Format:** [OpenAPI/Swagger/Markdown/etc.]
```

## Code Comments & JSDoc

```
Add comprehensive documentation comments to this code:

```[language]
[Paste code that needs documentation]
```

**Requirements:**
- Function/method descriptions
- Parameter descriptions with types
- Return value documentation
- Usage examples
- Error conditions
- Performance considerations (if relevant)

**Style:** [JSDoc/Sphinx/etc.]
```

## Architecture Documentation

```
Create architecture documentation for [SYSTEM/MODULE].

**Current State:**
- [Brief description of what exists]
- [Key components]
- [Main data flows]

**Documentation needed:**
- System overview diagram
- Component relationships
- Data flow documentation
- Decision rationale
- Future considerations

**Audience:** [Developers/Architects/Stakeholders]
**Format preference:** [Markdown/Diagrams/etc.]
```