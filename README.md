# env-doctor

A small CLI that compares `.env.example` with `.env` and reports missing, extra, or empty keys.

Use it in local setup or CI so new contributors (and future you) know which environment variables still need values.

## Requirements

- Python 3.10+

## Install

```bash
python -m pip install -e .
```

## Usage

From a project directory that contains both files:

```bash
env-doctor
```

Point at another directory:

```bash
env-doctor --path ./apps/api
```

JSON output (for scripts):

```bash
env-doctor --json
```

Exit codes:

| Code | Meaning |
|------|---------|
| 0 | All example keys are present and non-empty in `.env` |
| 1 | Missing keys, empty values, or extra keys (with `--strict-extra`) |
| 2 | Required files not found |

## Example

`.env.example`:

```
DATABASE_URL=
API_TOKEN=
```

`.env`:

```
DATABASE_URL=postgres://localhost:5432/app
```

```text
env-doctor: 1 missing, 1 empty
  missing: API_TOKEN
  empty:   DATABASE_URL (in example only — copy and fill .env)
```

## Development

```bash
python -m pip install -e ".[dev]"
python -m pytest
```

## License

MIT
