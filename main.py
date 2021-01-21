"""Ваша задача: починить адресную книгу, используя регулярные выражения.
Структура данных будет всегда:
lastname,firstname,surname,organization,position,phone,email
Предполагается, что телефон и e-mail у человека может быть только один.
Необходимо:

поместить Фамилию, Имя и Отчество человека в поля lastname, firstname и surname соответственно.
В записной книжке изначально может быть Ф + ИО, ФИО, а может быть сразу правильно: Ф+И+О;
привести все телефоны в формат +7(999)999-99-99.
Если есть добавочный номер, формат будет такой: +7(999)999-99-99 доб.9999;
объединить все дублирующиеся записи о человеке в одну.
телефон = (\+7|8)\s?\(?(\d{3})\)?[-\s]?(\d{3})[-\s]?(\d{2})[-\s]?(\d{2})[,\s]\(?([а-яё]+\.)?\s?(\d+)?\)?
"""

import re
from pprint import pprint
from collections import defaultdict
# читаем адресную книгу в формате CSV в список contacts_list
import csv
with open("phonebook_raw.csv", encoding = 'utf-8') as f:
  rows = csv.reader(f, delimiter=",")
  contacts_list = list(rows)
# pprint(contacts_list)

list_sorted = []
pattern_d = re.compile('\w+')
pattern_phone = re.compile(
        '(\+7|8)\s?\(?(\d{3})\)?[-\s]?(\d{3})[-\s]?(\d{2})[-\s]?(\d{2})[,\s]?\(?([а-яё]+\.)?\s?(\d+)?\)?')

def sorted_data(n):
    for data in contacts_list:
        list_sorted.insert(n,[])
        name = pattern_d.findall(data[0])
        list_sorted[n].insert(0,name.pop(0))
        if len(name) > 1:
            list_sorted[n].insert(1,name.pop(0))
        if len(name) > 0:
            list_sorted[n].insert(2,name.pop(0))
        last_name = pattern_d.findall(data[1])
        if len(last_name) > 1:
            list_sorted[n].insert(1, last_name.pop(0))
        if len(last_name) > 0:
            list_sorted[n].insert(2, last_name.pop(0))
        patronymic = pattern_d.findall(data[2])
        if len(patronymic) > 0:
            list_sorted[n].insert(2, patronymic.pop(0))
        n+=1
    return list_sorted

def merge_lists(data_list):
    for i,elem in enumerate(data_list):
        elem.extend(contacts_list[i][3:])
    return data_list

def edit_phone(list_):
    for elem in list_:
        result = re.sub(pattern_phone, r'+7(\2)\3-\4-\5 \6\7', elem[5])
        elem[5]=result
    return list_

# pprint(edit_phone(merge_lists(sorted_data(0))))

data = defaultdict(list)

for info in edit_phone(merge_lists(sorted_data(0))):
    key = tuple(info[:2])
    for item in info:
        if item not in data[key]:
            data[key].append(item)

new_list = list(data.values())
# pprint(new_list)

with open("phonebook.csv", "w") as f:
  datawriter = csv.writer(f, delimiter=',')
  # Вместо contacts_list подставьте свой список
  datawriter.writerows(new_list)
