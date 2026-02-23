"""Vigil core — runner, decorators, results, config."""

from vigil.core.results import TestResult
from vigil.core.decorators import test
from vigil.core.config import VigilConfig, load_config

__all__ = ["TestResult", "test", "VigilConfig", "load_config"]
