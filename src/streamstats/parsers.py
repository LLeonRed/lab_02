import csv
import json

from .errors import UnsupportedFormatError


def reading(file, format):
    #Открытие файла и проверка формата
    with open(file, "r", encoding="utf-8") as f:
        if format == "jsonl":
            for line in f:
                #Построчное чтение JSONL файла
                try:
                    data = json.loads(line)
                    yield [data, file]
                except:
                    yield ["Wrong format", file]
        elif format == "csv":
            reader = csv.reader(f)
            title = ""
            for row in reader:
                #Построчное чтение CSV файла
                if not title:
                    #Формирование первой строки-заголовка
                    title = [i for i in row]
                else:
                    try:
                        yield [{title[i]: row[i] for i in range(len(row))}, file]
                    except:
                        yield ["Wrong format", file]
        else:
            raise UnsupportedFormatError(f"Wrong Format in {file}")
