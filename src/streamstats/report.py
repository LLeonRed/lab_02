import json


def form_statistica(events, report):
    #Проверка на пропущенные строки
    if events[1]>0:
        events[0]['skipped_strings']=events[1]
    with open(report, "w", encoding='utf-8') as file:
        #Запись в JSON отчет
        file.write("[\n")
        json.dump(events[0], file, ensure_ascii=False, indent=4)
        file.write("\n]")
    return 0
