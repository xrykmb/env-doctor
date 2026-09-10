from __future__ import annotations

from pathlib import Path


def parse_env_file(path: Path) -> dict[str, str]:
    """Parse KEY=VALUE lines. Comments and blank lines are ignored."""
    values: dict[str, str] = {}
    if not path.exists():
        raise FileNotFoundError(str(path))

    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export ") :].strip()
        if "=" not in line:
            continue
        key, _, rest = line.partition("=")
        key = key.strip()
        if not key:
            continue
        value = rest.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
            value = value[1:-1]
        values[key] = value
    return values
