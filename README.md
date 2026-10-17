# StreamStats

Потоковый анализатор событий из файлов CSV и JSONL. Программа собирает статистику по уровням событий, источникам и временным меткам, сохраняя результат в JSON.

## Установка

Установка poetry:

```bash
poetry install
```

Создание окружения:

```bash
poetry env activate
```

## Использование

Анализ JSONL:

```bash
python -m streamstats analyze events.jsonl --format jsonl --output report.json
```

Анализ CSV:

```bash
run python -m streamstats analyze events.csv --format csv --output report.json
```

Анализ нескольких файлов:

```bash
python -m streamstats analyze file1.jsonl file2.jsonl --format jsonl --output report.json
```

Статистика всех переданных файлов объединяется в один отчёт.

### Обработка ошибок

По умолчанию программа останавливается при обнаружении некорректного события.

Чтобы пропускать ошибочные строки и продолжать обработку, используйте `--skip-invalid`:

```bash
python -m streamstats analyze events.jsonl --format jsonl --output report.json --skip-invalid
```

## Формат входных данных

Каждое событие должно содержать поля `timestamp`, `level`, `source` и `message`.

Пример JSONL:

```json
{"timestamp":"2026-10-17T10:00:00","level":"INFO","source":"server","message":"Started"}
{"timestamp":"2026-10-17T10:05:00","level":"ERROR","source":"database","message":"Connection failed"}
```

Допустимые уровни: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`.

## Тестирование

```bash
python -m pytest
python -m ruff check .
```

## Справка

```bash
python -m streamstats --help
```