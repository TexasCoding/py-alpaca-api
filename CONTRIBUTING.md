# Contributing to py-alpaca-api

Thank you for your interest in contributing to py-alpaca-api! This guide will help you get started.

## Development Setup

### Prerequisites
- Python 3.10 or higher
- [uv](https://github.com/astral-sh/uv) package manager

### Getting Started

1. Fork and clone the repository:
```bash
git clone https://github.com/yourusername/py-alpaca-api.git
cd py-alpaca-api
```

2. Install dependencies:
```bash
make install
```

3. Set up pre-commit hooks:
```bash
make pre-commit
```

4. Set up environment variables:
```bash
export ALPACA_API_KEY=your_api_key
export ALPACA_SECRET_KEY=your_secret_key
```

## Development Workflow

### Code Quality Tools

We use several tools to maintain code quality:

- **Ruff**: For linting and formatting
- **MyPy**: For static type checking
- **Pre-commit**: For automatic checks before commits

### Common Commands

Use the Makefile for common development tasks:

```bash
# Run tests
make test

# Format code
make format

# Run linter
make lint

# Fix linting issues
make lint-fix

# Run type checker
make type-check

# Run all checks
make check

# Clean build artifacts
make clean
```

### Testing

Run tests with:
```bash
./test.sh  # Runs all tests with API credentials
make test  # Alternative way
```

Run specific tests:
```bash
./test.sh tests/test_trading/test_orders.py
```

Generate coverage report:
```bash
make coverage
```

### Code Style

- Follow PEP 8 guidelines
- Use type hints for all function signatures
- Write docstrings for all public functions and classes (Google style)
- Keep line length under 88 characters
- Use meaningful variable and function names

### Pre-commit Hooks

Pre-commit hooks will automatically run before each commit to ensure code quality:

- Trailing whitespace removal
- End-of-file fixing
- YAML/JSON/TOML validation
- Ruff linting and formatting
- MyPy type checking

If pre-commit fails, fix the issues and try committing again.

## Making Changes

### Workflow

1. Create a new branch:
```bash
git checkout -b feature/your-feature-name
```

2. Make your changes and ensure tests pass:
```bash
make check
make test
```

3. Commit your changes:
```bash
git add .
git commit -m "feat: add new feature"
```

4. Push to your fork:
```bash
git push origin feature/your-feature-name
```

5. Create a pull request

### Commit Messages

Follow conventional commit format:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes
- `refactor:` Code refactoring
- `test:` Test changes
- `chore:` Maintenance tasks

## Pull Request Process

1. Ensure all tests pass
2. Update documentation if needed
3. Add tests for new functionality
4. Ensure your code follows the project style
5. Update the changelog if applicable
6. Request review from maintainers

## Project Structure

```
py-alpaca-api/
├── src/
│   └── py_alpaca_api/
│       ├── __init__.py          # Main API entry point
│       ├── exceptions.py        # Custom exceptions
│       ├── http/               # HTTP request handling
│       ├── models/             # Data models
│       ├── stock/              # Stock market operations
│       └── trading/            # Trading operations
├── tests/                      # Test files
├── docs/                       # Documentation
├── Makefile                    # Development commands
├── pyproject.toml             # Project configuration
└── .pre-commit-config.yaml    # Pre-commit hooks
```

## Getting Help

- Open an issue for bugs or feature requests
- Join discussions in existing issues
- Ask questions in pull requests

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.
