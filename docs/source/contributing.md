# Contributing

We welcome contributions to PyAlpacaAPI! This guide will help you get started.

## Getting Started

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally:
```bash
git clone https://github.com/YOUR_USERNAME/py-alpaca-api.git
cd py-alpaca-api
```

### Development Setup

```bash
# Install uv package manager
pip install uv

# Install dependencies
uv sync --all-extras --dev

# Install pre-commit hooks
pre-commit install

# Create .env file with API credentials
echo "ALPACA_API_KEY=your_api_key" >> .env
echo "ALPACA_SECRET_KEY=your_secret_key" >> .env
```

## Development Workflow

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### 2. Make Changes

Follow the project's coding standards:
- Use type hints for all functions
- Write docstrings (Google style)
- Keep line length under 88 characters
- Follow existing patterns in the codebase

### 3. Run Quality Checks

```bash
# Format code
make format

# Run linting
make lint

# Run type checking
make type-check

# Or run all checks at once
make check
```

### 4. Write Tests

Add tests for your changes:

```python
# tests/test_your_feature.py
import pytest
from py_alpaca_api import PyAlpacaAPI

def test_your_feature(alpaca):
    """Test description"""
    # Arrange
    expected = "expected_result"

    # Act
    result = your_function()

    # Assert
    assert result == expected
```

### 5. Run Tests

```bash
# Run all tests
./test.sh

# Run specific test file
./test.sh tests/test_your_feature.py

# Run with coverage
uv run pytest --cov=py_alpaca_api --cov-report=html
```

### 6. Commit Changes

```bash
# Stage changes
git add .

# Commit with conventional format
git commit -m "feat: Add new feature"
# or
git commit -m "fix: Fix bug in module"
```

Commit message format:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `test:` Test additions/changes
- `refactor:` Code refactoring
- `style:` Code style changes
- `perf:` Performance improvements
- `chore:` Maintenance tasks

### 7. Push and Create PR

```bash
# Push to your fork
git push origin feature/your-feature-name

# Create Pull Request on GitHub
```

## Code Standards

### Type Hints

Always use type hints:

```python
def get_quote(
    self,
    symbol: str,
    feed: str | None = None
) -> QuoteModel:
    """Get latest quote for symbol."""
    ...
```

### Docstrings

Use Google style docstrings:

```python
def calculate_return(
    initial_value: float,
    final_value: float
) -> float:
    """Calculate investment return percentage.

    Args:
        initial_value: Initial investment value
        final_value: Final investment value

    Returns:
        Return percentage as float

    Raises:
        ValueError: If initial_value is zero
    """
    if initial_value == 0:
        raise ValueError("Initial value cannot be zero")
    return (final_value - initial_value) / initial_value * 100
```

### Error Handling

Use custom exceptions:

```python
from py_alpaca_api.exceptions import ValidationError

def validate_quantity(qty: float) -> None:
    if qty <= 0:
        raise ValidationError(f"Quantity must be positive, got {qty}")
```

### Testing

Write comprehensive tests:

```python
class TestOrders:
    def test_market_order_valid(self, alpaca):
        """Test valid market order placement."""
        order = alpaca.trading.orders.market("AAPL", qty=1)
        assert order.symbol == "AAPL"
        assert order.qty == 1

    def test_market_order_invalid_qty(self, alpaca):
        """Test market order with invalid quantity."""
        with pytest.raises(ValidationError):
            alpaca.trading.orders.market("AAPL", qty=-1)
```

## Project Structure

Follow the existing structure:

```
src/py_alpaca_api/
├── trading/         # Trading operations
├── stock/          # Market data
├── models/         # Data models
├── cache/          # Caching system
├── http/           # HTTP layer
└── exceptions.py   # Custom exceptions
```

## Pull Request Guidelines

### PR Checklist

- [ ] Code follows project style
- [ ] All tests pass
- [ ] Type checking passes
- [ ] Documentation updated
- [ ] Changelog updated
- [ ] Commit messages follow convention
- [ ] PR description explains changes

### PR Description Template

```markdown
## Summary
Brief description of changes

## Changes
- Change 1
- Change 2

## Testing
How to test the changes

## Breaking Changes
Any breaking changes (if applicable)

## Related Issues
Fixes #123
```

## Testing Guidelines

### Test Categories

1. **Unit Tests**: Test individual functions
2. **Integration Tests**: Test API interactions
3. **Mock Tests**: Test without API calls

### Test Markers

```python
@pytest.mark.slow  # Slow tests
@pytest.mark.integration  # Integration tests
@pytest.mark.ci_skip  # Skip in CI
@pytest.mark.rate_limited  # Rate limited tests
```

### Test Fixtures

```python
@pytest.fixture
def alpaca():
    """Create API instance for testing."""
    return PyAlpacaAPI(
        api_key=os.environ.get("ALPACA_API_KEY"),
        api_secret=os.environ.get("ALPACA_SECRET_KEY"),
        api_paper=True
    )
```

## Documentation

### Update Documentation

1. Update docstrings in code
2. Update relevant .md files in docs/
3. Update CLAUDE.md if needed
4. Update README.md for user-facing changes

### Build Documentation

```bash
# Build documentation locally
cd docs
make html

# View documentation
open build/html/index.html
```

## Release Process

1. Update version in `pyproject.toml`
2. Update CHANGELOG.md
3. Create git tag
4. GitHub Actions handles PyPI release

## Getting Help

- Open an issue for bugs
- Start a discussion for features
- Check existing issues first
- Join our Discord (if available)

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Provide constructive feedback
- Focus on the code, not the person

Thank you for contributing to PyAlpacaAPI!
