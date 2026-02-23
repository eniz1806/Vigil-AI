# Contributing to Vigil

Thanks for your interest in contributing! Vigil is an open-source project and we welcome contributions of all kinds.

## Getting Started

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/Vigil-AI.git
   cd Vigil-AI
   ```
3. Create a virtual environment and install in dev mode:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -e ".[dev,all]"
   ```
4. Run the tests to make sure everything works:
   ```bash
   pytest tests/ -v
   ```

## Development Workflow

1. Create a branch for your change:
   ```bash
   git checkout -b my-feature
   ```
2. Make your changes
3. Run linting and tests:
   ```bash
   ruff check src/vigil/
   pytest tests/ -v
   ```
4. Commit and push:
   ```bash
   git commit -m "Add my feature"
   git push origin my-feature
   ```
5. Open a pull request

## What to Contribute

### Good first issues
- Add a new assertion (look at `src/vigil/assertions/` for examples)
- Add a new model to the pricing table in `src/vigil/cost.py`
- Improve error messages
- Add examples in `examples/`

### Bigger contributions
- New agent types (e.g., WebSocket, gRPC)
- New report formats
- Performance improvements
- Documentation improvements

## Code Style

- We use [ruff](https://github.com/astral-sh/ruff) for linting
- Target Python 3.10+
- Line length: 100 characters
- Keep it simple — avoid over-engineering

## Adding an Assertion

1. Create or edit a file in `src/vigil/assertions/`
2. Follow the pattern of existing assertions:
   ```python
   def assert_something(result, expected, **kwargs):
       output = result.output if isinstance(result, TestResult) else str(result)
       if not some_condition:
           raise AssertionError("Descriptive error message")
   ```
3. Export it in `src/vigil/__init__.py`
4. Add tests in `tests/test_assertions.py`

## Adding a Model to Cost Tracking

Edit `src/vigil/cost.py` and add the model to `MODEL_PRICING`:

```python
"model-name": (input_price_per_million, output_price_per_million),
```

## Tests

- All changes must have tests
- Run `pytest tests/ -v` before submitting
- Tests should not require API keys (mock external calls)

## Pull Request Guidelines

- Keep PRs focused — one feature or fix per PR
- Write a clear description of what changed and why
- Make sure CI passes (linting + tests)
- Update CHANGELOG.md if adding a feature or fixing a bug

## Questions?

Open an issue or start a discussion. We're happy to help!
