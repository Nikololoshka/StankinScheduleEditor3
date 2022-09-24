import os
import json

first_dir = "Расписания от 09.09.22 v2"
second_dir = "Расписания от 09.09.22 v3"

first_lst = set()
second_lst = set()


def find_files(dir, lst):
    for dirpath, dirnames, filenames in os.walk(dir):
        for filename in filenames:
            if filename.endswith(".json"):
                lst.add(dirpath + os.sep + filename)


def ordered(obj):
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj


def dates_eq(a, b):
    for date_1 in a:
        finded = False
        for date_2 in b:
            if date_1['frequency'] == date_2['frequency'] and date_1['date'] == date_2['date']:
                finded = True
                break

        if not finded:
            # print("Не найдена дата: " + str(date_1))
            return False

    return True


def pair_eq(a, b):
    return a['title'] == b['title'] and \
           (a['lecturer'].replace('ё', 'е')) == (b['lecturer'].replace('ё', 'е')) and \
           a['classroom'] == b['classroom'] and \
           a['type'] == b['type'] and \
           a['subgroup'] == b['subgroup'] and \
           a['time']['start'] == b['time']['start'] and \
           a['time']['end'] == b['time']['end'] and \
           dates_eq(a['dates'], b['dates'])


def json_eq(a, b):
    for pair_1 in a:

        finded = False
        for pair_2 in b:
            if pair_eq(pair_1, pair_2):
                finded = True
                break

        if not finded:
            print("Не найдена пара: " + str(pair_1))
            return False

    return True


find_files(first_dir, first_lst)
find_files(second_dir, second_lst)

first_lst = sorted(first_lst)
second_lst = sorted(second_lst)

for first, second in zip(first_lst, second_lst):
    with open(first, 'r', encoding='utf-8') as first_file, open(second, 'r', encoding='utf-8') as second_file:
        first_json = json.load(first_file)
        second_json = json.load(second_file)

        eq = json_eq(first_json, second_json)
        if not eq:
            print(first, second)

            print('=' * 50)

        # is_right = ordered(first_json) == ordered(second_json)
        # if not is_right:
        #    print(first, 'and' , second)
