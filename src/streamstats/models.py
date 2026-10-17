from .errors import StreamStatsError
from .constants import LEVEL, STRUCTURE

def checking(event, skip, number, file):
        #skip Обозначает, что ошибочные строки пропускаются
        if len(event) != 4:
            #Проверка структуры
            if not skip:
                raise StreamStatsError(f"Wrong structure in string {number} in file {file}")
            else:
                return {"Wrong structure"}
        check_type = 0
        for i in event:
            #Проверка формата даты
            if check_type == 0:
                #Приведение даты к общему формату
                check_date = event[i].split("T")
                datestamp = check_date[0].split("-")
                timestamp = check_date[1].split(":")
                days30 = [4, 6, 9, 11]#месяца с 30 днями
                #Проверка всех ограничений
                if (
                    len(datestamp) != 3
                    or len(datestamp[1]) != 2
                    or len(datestamp[2]) != 2
                    or datestamp[0] == "0"
                    or int(datestamp[1]) > 12
                    or int(datestamp[1]) == 0
                    or int(datestamp[1]) > 31
                    or int(datestamp[2]) == 0
                    or (int(datestamp[1]) in days30 and int(datestamp[2]) > 30)
                    or (
                        int(datestamp[1]) == 2
                        and (
                            int(datestamp[2]) > 28
                            if int(datestamp[0]) % 4 != 0
                            else int(datestamp[2]) > 29
                        )
                    )
                ):
                    if not skip:
                        raise StreamStatsError(f"Wrong date in string {number} in file {file}")
                    else:
                        return {"Wrong date"}
                if (
                    len(timestamp) != 3
                    or int(timestamp[0]) > 24
                    or int(timestamp[1]) > 59
                    or int(timestamp[2]) > 59
                    or any(len(j) != 2 for j in timestamp)
                ):
                    if not skip:
                        raise StreamStatsError(f"Wrong date in string {number} in file {file}")
                    else:
                        return {"Wrong date"}
            elif check_type == 1:
                #Проверка на тип информации
                if event[i] not in LEVEL:
                    if not skip:
                        raise StreamStatsError(f"Wrong level in string {number} in file {file}")
                    else:
                        return {"Wrong level"}
            elif check_type == 2:
                #Проверка на непустой источник
                if not event[i]:
                    if not skip:
                        raise StreamStatsError(f"Empty source in string {number} in file {file}")
                    else:
                        return {"Empty source"}
            if i != STRUCTURE[check_type]:
                #Проверка формата структуры
                if not skip:
                    raise StreamStatsError(f"Wrong structure in string {number} in file {file}")
                else:
                    return {"Wrong structure"}
            check_type += 1
        return event
        


