# Installation

## Basic

```bash
pip install vigil-ai
```

## With extras

```bash
# OpenAI support (for LLM-as-judge, embeddings)
pip install "vigil-ai[openai]"

# Anthropic support
pip install "vigil-ai[anthropic]"

# HTTP agent testing
pip install "vigil-ai[http]"

# Parallel test execution
pip install "vigil-ai[parallel]"

# Everything
pip install "vigil-ai[all]"
```

## Requirements

- Python 3.10+
- No other system dependencies

## Verify installation

```bash
vigil --version
```
