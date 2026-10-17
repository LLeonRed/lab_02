import sys
import subprocess
import json
from pathlib import Path
import shutil
# Каталог с заранее подготовленными файлами
DATA = Path(__file__).parent / "data"


# Вспомогательная функция для запуска CLI
def run_cli(*args):
    return subprocess.run(
        [
            sys.executable,
            "-m", "streamstats",
            "analyze",
            *map(str, args)
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace"
    )


# 1. Тест пустого файла

def test_emptyfile(tmp_path):
    output = tmp_path / "report.json"

    result = run_cli(
        DATA / "empty.jsonl",
        "--format", "jsonl",
        "--output", output
    )

    assert result.returncode == 0, result.stderr

    report = json.loads(output.read_text(encoding="utf-8"))[0]

    assert report["events"] == 0
    assert report["level types"]["INFO"] == 0
    assert report["level types"]["ERROR"] == 0

#2. Unit-тест JSONL файла

def test_jsonl_parser(tmp_path):
    output = tmp_path / "report.json"

    result = run_cli(
        DATA / "events.jsonl",
        "--format", "jsonl",
        "--output", output
    )

    assert result.returncode == 0, result.stderr

    report = json.loads(output.read_text(encoding="utf-8"))[0]

    assert report["events"] == 2
    assert report["level types"]["INFO"] == 1
    assert report["level types"]["ERROR"] == 1
    assert report["source list"]["server"] == 1
    assert report["source list"]["database"] == 1
    assert report["error sources"]["database"] == 1

#3. Unit-тест CSV файла

def test_csv_parser(tmp_path):
    output = tmp_path / "report.json"

    result = run_cli(
        DATA / "events.csv",
        "--format", "csv",
        "--output", output
    )

    assert result.returncode == 0, result.stderr

    report = json.loads(output.read_text(encoding="utf-8"))[0]

    assert report["events"] == 2
    assert report["level types"]["INFO"] == 1
    assert report["level types"]["ERROR"] == 1
    assert report["source list"]["server"] == 1
    assert report["source list"]["database"] == 1
    assert report["error sources"]["database"] == 1



#4. Тест файла с ошибочной строкой без --invalid-skip
def test_invalid_without_skip(tmp_path):
    output = tmp_path / "report.json"

    result = run_cli(
        DATA / "invalid.jsonl",
        "--format", "jsonl",
        "--output", output
    )

    assert result.returncode == 2
    assert "invalid.jsonl" in result.stderr
    assert "2" in result.stderr


#5. Тест файла с ошибочной строкой c --invalid-skip
def test_invalid_with_skip(tmp_path):
    output = tmp_path / "report.json"

    result = run_cli(
        DATA / "invalid.jsonl",
        "--format", "jsonl",
        "--skip-invalid",
        "--output", output
    )

    assert result.returncode == 0, result.stderr

    report = json.loads(output.read_text(encoding="utf-8"))[0]

    assert report["events"] == 2
    assert report["level types"]["INFO"] == 1
    assert report["level types"]["ERROR"] == 1
    assert report["source list"]["server"] == 1
    assert report["source list"]["database"] == 1
    assert report["error sources"]["database"] == 1


#6. Тест нескольких файлов
def test_multiple_files(tmp_path):
    output = tmp_path / "report.json"

    result = run_cli(
        DATA / "events.jsonl",
        DATA / "events2.jsonl",
        "--format", "jsonl",
        "--output", output
    )

    assert result.returncode == 0, result.stderr

    report = json.loads(output.read_text(encoding="utf-8"))[0]

    assert report["events"] == 4

    assert report["level types"]["INFO"] == 1
    assert report["level types"]["ERROR"] == 1
    assert report["level types"]["WARNING"] == 1
    assert report["level types"]["CRITICAL"] == 1

    assert report["source list"]["server"] == 2
    assert report["source list"]["database"] == 2

    assert report["error sources"]["database"] == 2

    assert report["earliest time"] == "2026-10-17T10:00:00"
    assert report["latest time"] == "2026-10-17T11:10:00"


#7. Unicode тест
def test_unicode(tmp_path):
    output = tmp_path / "report.json"

    result = run_cli(
        DATA / "unicode.jsonl",
        "--format", "jsonl",
        "--output", output
    )

    assert result.returncode == 0, result.stderr

    report = json.loads(output.read_text(encoding="utf-8"))[0]

    assert report["events"] == 1
    assert report["source list"]["сервер"] == 1
    assert report["error sources"]["сервер"] == 1


#8. Интеграционный тест CLI
def test_cli_integration(tmp_path):
    input_file = tmp_path / "input.jsonl"
    output_file = tmp_path / "report.json"

    shutil.copyfile(DATA / "events.jsonl", input_file)

    result = run_cli(
        input_file,
        "--format", "jsonl",
        "--output", output_file
    )

    assert result.returncode == 0, result.stderr
    assert output_file.exists()

    report = json.loads(
        output_file.read_text(encoding="utf-8")
    )[0]

    assert report["events"] == 2
    assert report["level types"]["INFO"] == 1
    assert report["level types"]["ERROR"] == 1
    assert report["source list"]["server"] == 1
    assert report["source list"]["database"] == 1
    assert report["error sources"]["database"] == 1
