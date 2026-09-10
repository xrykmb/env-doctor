from pathlib import Path

from env_doctor.check import check_env_files
from env_doctor.cli import main
from env_doctor.parse import parse_env_file


def write_env(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def test_parse_ignores_comments_and_quotes(tmp_path: Path) -> None:
    write_env(
        tmp_path / ".env",
        """
# comment
export DATABASE_URL="postgres://local"
API_TOKEN='secret'
EMPTY=
NOEQUALS
=nokey
""",
    )
    parsed = parse_env_file(tmp_path / ".env")
    assert parsed["DATABASE_URL"] == "postgres://local"
    assert parsed["API_TOKEN"] == "secret"
    assert parsed["EMPTY"] == ""
    assert "NOEQUALS" not in parsed


def test_reports_missing_and_empty(tmp_path: Path) -> None:
    write_env(tmp_path / ".env.example", "A=\nB=\nC=\n")
    write_env(tmp_path / ".env", "A=1\nB=\nD=extra\n")
    result = check_env_files(tmp_path)
    assert result.missing == ("C",)
    assert result.empty == ("B",)
    assert result.extra == ("D",)
    assert result.ok is False


def test_ok_when_all_example_keys_filled(tmp_path: Path) -> None:
    write_env(tmp_path / ".env.example", "A=\n")
    write_env(tmp_path / ".env", "A=value\n")
    result = check_env_files(tmp_path)
    assert result.ok is True


def test_cli_json_and_exit_codes(tmp_path: Path, capsys) -> None:
    write_env(tmp_path / ".env.example", "TOKEN=\n")
    write_env(tmp_path / ".env", "TOKEN=abc\n")
    assert main(["--path", str(tmp_path), "--json"]) == 0
    out = capsys.readouterr().out
    assert '"ok": true' in out

    write_env(tmp_path / ".env", "")
    assert main(["--path", str(tmp_path)]) == 1
