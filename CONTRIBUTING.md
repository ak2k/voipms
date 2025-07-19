# Contributing to voipms

Thank you for your interest in contributing to voipms! This document provides guidelines for contributing to the project.

## Development Setup

1. Fork and clone the repository:
```bash
git clone https://github.com/your-username/voipms.git
cd voipms
```

2. Install dependencies using [uv](https://github.com/astral-sh/uv):
```bash
uv sync
```

3. Set up pre-commit hooks (optional but recommended):
```bash
uv run pre-commit install
```

## Making Changes

### Code Style

- We use `ruff` for linting and formatting
- Type hints are required for all public functions
- Run `uv run ruff check .` before committing
- Run `uv run mypy src/` to check types

### Testing

- Write tests for new functionality
- Ensure all tests pass: `uv run pytest`
- Aim for good test coverage

### Updating the API Definition

If VoIP.ms has added new methods or changed existing ones:

1. Update the source files in `resources/`:
   - Download the latest WSDL from VoIP.ms
   - Save the latest HTML documentation

2. Regenerate the API definition:
```bash
uv run python3 tools/generate_api_definition.py
```

3. Update type stubs:
```bash
uv run python3 tools/generate_type_stubs.py
```

4. Test the changes thoroughly

## Submitting Changes

1. Create a new branch for your changes:
```bash
git checkout -b feature/your-feature-name
```

2. Make your changes and commit them with clear messages:
```bash
git commit -m "feat: add support for new API method"
```

3. Push to your fork and submit a pull request

### Commit Message Guidelines

We follow conventional commits:

- `feat:` New features
- `fix:` Bug fixes
- `docs:` Documentation changes
- `style:` Code style changes (formatting, etc.)
- `refactor:` Code refactoring
- `test:` Test additions or changes
- `chore:` Maintenance tasks

## Pull Request Process

1. Ensure all tests pass
2. Update documentation if needed
3. Add a clear description of your changes
4. Link any related issues

## Questions?

Feel free to open an issue for any questions or concerns!