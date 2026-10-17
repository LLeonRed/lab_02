import csv
import json

from .errors import StreamStatsError


def reading(file, format):
    #Открытие файла и проверка формата
    with open(file, "r", encoding="utf-8") as f:
        if format == "jsonl":
            for line in f:
                #Построчное чтение JSONL файла
                data = json.loads(line)
                yield [data, file]
        elif format == "csv":
            reader = csv.reader(f)
            title = ""
            for row in reader:
                #Построчное чтение CSV файла
                if not title:
                    #Формирование первой строки-заголовка
                    title = [i for i in row]
                else:
                    if len(row)!=len(title):
                        yield ["Wrong format"]
                    else:
                        yield [{title[i]: row[i] for i in range(len(row))}, file]
        else:
            raise StreamStatsError(f"Wrong Format in {file}")
