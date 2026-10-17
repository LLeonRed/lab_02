import argparse
import sys

from .errors import StreamStatsError
from .analysis import form_statistic
from .models import checking
from .parsers import reading
from .report import form_statistica

parser = argparse.ArgumentParser()
#Создание субпарсера команд
subparser = parser.add_subparsers(dest="command", required=True)

#Добавление аргументов к парсеру
fparser = subparser.add_parser("analyze")
fparser.add_argument("files", nargs="+")

fparser.add_argument("--format", required=True, help="Choose format of the loaded files(jsonl or csv)")
fparser.add_argument("--output", required=True, help="Choose name for the report file in format '*.json'")
fparser.add_argument("--skip-invalid", required=False, action='count', help="Skip invalid strings and continue without breaking")

args = parser.parse_args()

#Проверка на правильность команды
if args.command == "analyze":
    result = []
    for i in args.files:
        #Прохождение по списку путей к файлам
        strn=1
        for j in reading(i, args.format):
            #Анализирование на ошибки
            try:
                result.append(checking(j[0], args.skip_invalid, strn, j[1]))
                strn+=1
            except StreamStatsError as error:
                #Вывод ошибки и кода ошибки
                print(error, file=sys.stderr)
                sys.exit(2)
    if form_statistic(result)[1]>0:
        print(f"WARNING! {form_statistic(result)[1]} strings were skipped")
    form_statistica(form_statistic(result), args.output)
else:
    print("Wrong comand")