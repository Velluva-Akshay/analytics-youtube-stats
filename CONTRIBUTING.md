# Contributing to YouTube Analytics

Thank you for considering contributing to this project! Here are some guidelines to help you get started.

## Development Setup

1. Fork and clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r analytics_project/requirements.txt
   ```

## Running Tests

Run the full test suite:
```bash
cd analytics_project
pytest tests/ -v
```

Run specific test file:
```bash
pytest tests/test_analysis.py -v
```

Run with coverage:
```bash
pytest tests/ --cov=src --cov-report=html
```

## Code Style

- Follow PEP 8 guidelines
- Use type hints where appropriate
- Add docstrings to all public functions and classes
- Keep functions focused and under 50 lines when possible

## Adding New Features

1. Create a new branch: `git checkout -b feature/your-feature-name`
2. Write tests first (TDD approach recommended)
3. Implement the feature
4. Ensure all tests pass
5. Update documentation if needed
6. Submit a pull request

## Project Structure

```
analytics_project/
├── src/                  # Core modules
│   ├── load_data.py     # Data loading utilities
│   ├── eda.py           # Exploratory data analysis
│   ├── analysis.py      # Advanced analytics
│   ├── validation.py    # Data quality checks
│   ├── config.py        # Configuration management
│   └── cli.py           # Command-line interface
├── tests/               # Test suite
├── notebooks/           # Jupyter notebooks
├── outputs/             # Generated artifacts (gitignored)
└── config.yaml          # Configuration file
```

## Testing Guidelines

- Write unit tests for all new functions
- Aim for >80% code coverage
- Use fixtures for common test data
- Test both success and failure cases
- Mock external dependencies

## Documentation

- Update README.md for user-facing changes
- Add docstrings following Google style
- Include code examples in docstrings
- Update CHANGELOG.md with notable changes

## Reporting Issues

When reporting bugs, please include:
- Python version
- Operating system
- Steps to reproduce
- Expected vs actual behavior
- Error messages/stack traces

## Feature Requests

For new features:
- Explain the use case
- Provide examples if possible
- Consider backward compatibility

## Questions?

Open an issue or discussion on GitHub!
