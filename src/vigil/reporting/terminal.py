"""Rich terminal reporter."""

from __future__ import annotations

from typing import Any

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text


class TerminalReporter:
    """Renders test results in the terminal using Rich."""

    def __init__(self, verbose: bool = False) -> None:
        self.console = Console()
        self.verbose = verbose
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

    def render(self) -> None:
        self.console.print()

        # Header
        self.console.print(
            Panel.fit(
                "[bold]Vigil[/bold] — AI Agent Test Results",
                border_style="blue",
            )
        )
        self.console.print()

        # Results table
        table = Table(show_header=True, header_style="bold")
        table.add_column("Status", width=4, justify="center")
        table.add_column("Test", min_width=30)
        table.add_column("Duration", justify="right", width=10)
        table.add_column("Cost", justify="right", width=10)
        table.add_column("Tokens", justify="right", width=10)

        for r in self.results:
            status = Text("PASS", style="green bold") if r["passed"] else Text("FAIL", style="red bold")
            duration = f"{r['duration']:.2f}s" if r["duration"] else "-"
            cost = f"${r['cost']:.4f}" if r["cost"] is not None else "-"
            tokens = str(r["tokens"]) if r["tokens"] is not None else "-"
            table.add_row(status, r["name"], duration, cost, tokens)

        self.console.print(table)
        self.console.print()

        # Summary
        passed = sum(1 for r in self.results if r["passed"])
        failed = sum(1 for r in self.results if not r["passed"])
        total = len(self.results)
        total_cost = sum(r["cost"] for r in self.results if r["cost"] is not None)
        total_duration = sum(r["duration"] for r in self.results)

        if failed == 0:
            summary_style = "green"
            summary_text = f"All {total} tests passed"
        else:
            summary_style = "red"
            summary_text = f"{failed} failed, {passed} passed out of {total}"

        self.console.print(
            f"[bold {summary_style}]{summary_text}[/bold {summary_style}] "
            f"| {total_duration:.2f}s total"
            f"{f' | ${total_cost:.4f} total cost' if total_cost > 0 else ''}"
        )

        # Show errors in verbose mode
        if self.verbose:
            for r in self.results:
                if r["error"]:
                    self.console.print(f"\n[red bold]FAIL[/red bold] {r['name']}:")
                    self.console.print(f"  {r['error']}")

        self.console.print()
