# Installation

## Basic

```bash
pip install vigil-eval
```

## With extras

```bash
# OpenAI support (for LLM-as-judge, embeddings)
pip install "vigil-eval[openai]"

# Anthropic support
pip install "vigil-eval[anthropic]"

# HTTP agent testing
pip install "vigil-eval[http]"

# Parallel test execution
pip install "vigil-eval[parallel]"

# Everything
pip install "vigil-eval[all]"
```

## Requirements

- Python 3.10+
- No other system dependencies

## Verify installation

```bash
vigil --version
```
