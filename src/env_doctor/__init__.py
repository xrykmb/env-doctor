"""Compare .env.example with .env."""

from .check import CheckResult, check_env_files

__all__ = ["CheckResult", "check_env_files"]
__version__ = "0.1.0"
