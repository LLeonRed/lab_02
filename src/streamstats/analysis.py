from .constants import LEVEL, STRUCTURE


def form_statistic(events):
    #Ввод переменных для итогового формата
    skip=0
    errors = {}
    level_counter = {i: 0 for i in LEVEL}
    source_counter = {}
    firsttime = ''
    curfi=float("+inf")
    lasttime = ''
    curla=0
    counter = 0
    for i in events:
        #Прохождение по событиям
        if len(i)==1:
            #Проверка на пропущенные строки с ошибками
            skip+=1
        else:
            error = False #Идентификатор ошибки
            counter += 1 #Подсчет всех строк
            for j in i:
                if j == STRUCTURE[0]:
                    #Нахождение наибольшего и наименьшего времени
                    m = int(i[j].replace("-", "").replace(":", "").replace("T", ""))
                    if m<curfi:
                        firsttime=i[j]
                        curfi=m
                    if m>curla:
                        lasttime=i[j]
                        curla=m
                elif j == STRUCTURE[1]:
                    #Проверка типа сообщения
                    if i[j] == "ERROR" or i[j] == "CRITICAL":
                        error = True #Обозначение ошибки
                    level_counter[i[j]] += 1 #Подсчет количества типов
                elif j == STRUCTURE[2]:
                    if error:
                        #Подсчет источников ошибок
                        if i[j] not in errors:
                            errors[i[j]] = 1
                        else:
                            errors[i[j]] += 1
                    #Подсчет источников
                    if i[j] not in source_counter:
                        source_counter[i[j]] = 1
                    else:
                        source_counter[i[j]] += 1
    errors = sorted([[errors[elem], elem] for elem in errors])[-5:] #Оставление 5 самых частых источников ошибок
    errors = {k[1]: k[0] for k in errors}
    return [{
        "events": counter,
        "level types": level_counter,
        "source list": source_counter,
        "error sources": errors,
        "earliest time": firsttime if curfi != float('+inf') else 0,
        "latest time": lasttime,
    }, skip]
