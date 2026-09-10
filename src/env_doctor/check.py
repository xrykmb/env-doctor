from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .parse import parse_env_file


@dataclass(frozen=True)
class CheckResult:
    missing: tuple[str, ...]
    empty: tuple[str, ...]
    extra: tuple[str, ...]

    @property
    def ok(self) -> bool:
        return not self.missing and not self.empty


def check_env_files(
    directory: Path,
    *,
    example_name: str = ".env.example",
    env_name: str = ".env",
) -> CheckResult:
    example_path = directory / example_name
    env_path = directory / env_name
    example = parse_env_file(example_path)
    actual = parse_env_file(env_path)

    missing = tuple(sorted(k for k in example if k not in actual))
    empty = tuple(sorted(k for k, v in actual.items() if k in example and v == ""))
    extra = tuple(sorted(k for k in actual if k not in example))
    return CheckResult(missing=missing, empty=empty, extra=extra)
