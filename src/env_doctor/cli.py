from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .check import check_env_files


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="env-doctor",
        description="Compare .env.example with .env and report missing or empty keys.",
    )
    parser.add_argument(
        "--path",
        default=".",
        help="Directory that contains the env files (default: current directory)",
    )
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON")
    parser.add_argument(
        "--strict-extra",
        action="store_true",
        help="Treat keys present in .env but missing from .env.example as errors",
    )
    args = parser.parse_args(argv)

    directory = Path(args.path).resolve()
    try:
        result = check_env_files(directory)
    except FileNotFoundError as exc:
        print(f"env-doctor: file not found: {exc}", file=sys.stderr)
        return 2

    if args.json:
        print(
            json.dumps(
                {
                    "ok": result.ok and not (args.strict_extra and result.extra),
                    "missing": list(result.missing),
                    "empty": list(result.empty),
                    "extra": list(result.extra),
                }
            )
        )
    else:
        _print_human(result)

    failed = bool(result.missing or result.empty)
    if args.strict_extra and result.extra:
        failed = True
    return 1 if failed else 0


def _print_human(result) -> None:
    if result.ok:
        extra_note = f", {len(result.extra)} extra" if result.extra else ""
        print(f"env-doctor: ok{extra_note}")
        if result.extra:
            print("  extra:   " + ", ".join(result.extra))
        return

    print(
        f"env-doctor: {len(result.missing)} missing, {len(result.empty)} empty"
        + (f", {len(result.extra)} extra" if result.extra else "")
    )
    if result.missing:
        print("  missing: " + ", ".join(result.missing))
    if result.empty:
        print("  empty:   " + ", ".join(result.empty))
    if result.extra:
        print("  extra:   " + ", ".join(result.extra))


if __name__ == "__main__":
    raise SystemExit(main())
