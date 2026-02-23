# Changelog

All notable changes to Vigil will be documented in this file.

## [0.2.3] - 2026-02-23

### Added
- Comparison table in README (vs DeepEval, Promptfoo, RAGAS)
- CI workflow with ruff linting and Python 3.10-3.13 testing
- CI badge in README

### Fixed
- Unused imports flagged by ruff

## [0.2.2] - 2026-02-23

### Fixed
- Logo URLs in README updated to absolute paths for PyPI rendering

## [0.2.1] - 2026-02-23

### Changed
- Package renamed from `vigil-ai` to `vigil-eval` on PyPI
- All install references updated across docs, source, and examples

## [0.2.0] - 2026-02-23

### Added
- **Plugin system** — `register_assertion`, `register_agent`, `register_reporter` decorators with entry point discovery
- **LLM-as-judge** — `assert_quality` (single criteria) and `assert_rubric` (multi-criteria) using OpenAI or Anthropic
- **Async support** — `arun()` method on FunctionAgent, HTTPAgent, and CLIAgent
- **Embedding-based semantic matching** — OpenAI `text-embedding-3-small` support in `assert_semantic_match`
- **Cost tracking** — auto-calculate API costs for 20+ models across OpenAI, Anthropic, Google, DeepSeek
- **`vigil init` command** — scaffold a new project with config, example test, and CI workflow
- **pyproject.toml config** — `[tool.vigil]` section support as alternative to `vigil.yaml`
- **Parallel execution** — `--parallel N` flag using pytest-xdist
- **GitHub Action** — composite action for CI integration
- **Documentation site** — 11 pages built with mkdocs-material

## [0.1.0] - 2026-02-23

### Added
- Core framework with `@test()` decorator and test runner
- `TestResult` dataclass with output, cost, tokens, latency, model, metadata
- **7 assertions**: `assert_contains`, `assert_not_contains`, `assert_json_valid`, `assert_matches_regex`, `assert_cost_under`, `assert_tokens_under`, `assert_latency_under`
- **Semantic matching**: `assert_semantic_match` with word overlap and cosine similarity
- **Hallucination detection**: `assert_no_hallucination` with sentence-level grounding
- **3 agent types**: `FunctionAgent`, `HTTPAgent`, `CLIAgent`
- **Snapshot testing**: save golden outputs, compare on subsequent runs
- **Reporting**: Rich terminal output and standalone HTML reports
- **CLI**: `vigil run`, `vigil snapshot update/list`, `vigil report`
- **Config**: `vigil.yaml` loader with defaults
- **pytest plugin**: auto-registered via entry point
- 59 unit tests
- Examples: basic, OpenAI agent, multi-step workflow
