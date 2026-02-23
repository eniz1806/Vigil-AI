"""HTML report generator."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


_HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Vigil Test Report</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0d1117; color: #c9d1d9; padding: 2rem; }
  .header { text-align: center; margin-bottom: 2rem; }
  .header h1 { font-size: 2rem; color: #58a6ff; }
  .header .timestamp { color: #8b949e; font-size: 0.9rem; margin-top: 0.5rem; }
  .summary { display: flex; gap: 1rem; justify-content: center; margin-bottom: 2rem; }
  .stat { background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 1rem 2rem; text-align: center; }
  .stat .value { font-size: 1.5rem; font-weight: bold; }
  .stat .label { color: #8b949e; font-size: 0.85rem; }
  .stat.pass .value { color: #3fb950; }
  .stat.fail .value { color: #f85149; }
  .stat.cost .value { color: #d2a8ff; }
  table { width: 100%; border-collapse: collapse; background: #161b22; border-radius: 8px; overflow: hidden; }
  th { background: #21262d; text-align: left; padding: 0.75rem 1rem; font-weight: 600; color: #8b949e; }
  td { padding: 0.75rem 1rem; border-top: 1px solid #21262d; }
  .pass-badge { color: #3fb950; font-weight: bold; }
  .fail-badge { color: #f85149; font-weight: bold; }
  .error { color: #f85149; font-size: 0.85rem; margin-top: 0.25rem; }
</style>
</head>
<body>
<div class="header">
  <h1>Vigil Test Report</h1>
  <div class="timestamp">{{TIMESTAMP}}</div>
</div>
<div class="summary">
  <div class="stat pass"><div class="value">{{PASSED}}</div><div class="label">Passed</div></div>
  <div class="stat fail"><div class="value">{{FAILED}}</div><div class="label">Failed</div></div>
  <div class="stat"><div class="value">{{DURATION}}</div><div class="label">Duration</div></div>
  <div class="stat cost"><div class="value">{{COST}}</div><div class="label">Total Cost</div></div>
</div>
<table>
  <thead><tr><th>Status</th><th>Test</th><th>Duration</th><th>Cost</th><th>Tokens</th></tr></thead>
  <tbody>{{ROWS}}</tbody>
</table>
</body>
</html>"""


class HTMLReporter:
    """Generates a standalone HTML test report."""

    def __init__(self) -> None:
        self.results: list[dict[str, Any]] = []

    def add_result(
        self,
        name: str,
        passed: bool,
        duration: float = 0,
        cost: float | None = None,
        tokens: int | None = None,
        error: str | None = None,
    ) -> None:
        self.results.append({
            "name": name,
            "passed": passed,
            "duration": duration,
            "cost": cost,
            "tokens": tokens,
            "error": error,
        })

    def render(self, output_path: str | Path = "vigil-report.html") -> Path:
        path = Path(output_path)

        passed = sum(1 for r in self.results if r["passed"])
        failed = sum(1 for r in self.results if not r["passed"])
        total_cost = sum(r["cost"] for r in self.results if r["cost"] is not None)
        total_duration = sum(r["duration"] for r in self.results)

        rows = ""
        for r in self.results:
            badge = '<span class="pass-badge">PASS</span>' if r["passed"] else '<span class="fail-badge">FAIL</span>'
            dur = f"{r['duration']:.2f}s" if r["duration"] else "-"
            cost = f"${r['cost']:.4f}" if r["cost"] is not None else "-"
            tokens = str(r["tokens"]) if r["tokens"] is not None else "-"
            error_html = f'<div class="error">{r["error"]}</div>' if r["error"] else ""
            rows += f"<tr><td>{badge}</td><td>{r['name']}{error_html}</td><td>{dur}</td><td>{cost}</td><td>{tokens}</td></tr>\n"

        html = _HTML_TEMPLATE
        html = html.replace("{{TIMESTAMP}}", datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"))
        html = html.replace("{{PASSED}}", str(passed))
        html = html.replace("{{FAILED}}", str(failed))
        html = html.replace("{{DURATION}}", f"{total_duration:.2f}s")
        html = html.replace("{{COST}}", f"${total_cost:.4f}")
        html = html.replace("{{ROWS}}", rows)

        path.write_text(html)
        return path

    def to_json(self) -> str:
        return json.dumps({
            "results": self.results,
            "summary": {
                "passed": sum(1 for r in self.results if r["passed"]),
                "failed": sum(1 for r in self.results if not r["passed"]),
                "total_cost": sum(r["cost"] for r in self.results if r["cost"] is not None),
            },
        }, indent=2)
