#!/usr/bin/env python
# coding: utf-8

# ### Домашнее задание к лекции 2.2 «Regular expressions»
# Иногда при знакомстве мы записываем контакты в адресную книгу кое-как с мыслью, что "когда-нибудь потом все обязательно поправим". Копируем данные из интернета или из смски. Добавляем людей в разных мессенджерах. В результате получается адресная книга, в которой совершенно невозможно кого-то нормально найти: мешает множество дублей, разная запись одних и тех же имен и телефонов.
# 
# Кейс основан на реальных данных из https://www.nalog.ru/opendata/, https://www.minfin.ru/ru/opendata/
# 
# Ваша задача: привести в порядок адресную книгу, используя регулярные выражения.
# Структура данных будет всегда такая:
# lastname,firstname,surname,organization,position,phone,email
# 
# Предполагается, что:
# 
# телефон и e-mail у одного человека может быть только один;
# если совпали одновременно Фамилия и Имя, это точно один и тот же человек (даже если не указано его отчество).
# Ваша задача:
# 
# 1. Поместить Фамилию, Имя и Отчество человека в поля lastname, firstname и surname соответственно. В записной книжке изначально может быть Ф + ИО, ФИО, а может быть сразу правильно: Ф+И+О. Подсказка: работайте со срезом списка (три первых элемента) при помощи " ".join([:2]) и split(" "), регулярки здесь НЕ НУЖНЫ.
# 
# 2. Привести все телефоны в формат +7(999)999-99-99. Если есть добавочный номер, формат будет такой: +7(999)999-99-99 доб.9999. Подсказка: используйте регулярки для обработки телефонов.
# 
# 3. Объединить все дублирующиеся записи о человеке в одну. Подсказка: группируйте записи по ФИО (если будет сложно, допускается группировать только по ФИ).
# 

# In[1]:


import re
import csv
from pprint import pprint


# In[2]:


with open("D:/Python-developer/Python/RegEx/phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)
pprint(contacts_list)


# In[18]:


pattern = r"(\+7|8)*[\s\(]*(\d{3})[\)\s-]*(\d{3})[-]*(\d{2})[-]*(\d{2})[\s\(]*(доб\.)*[\s]*(\d+)*[\)]*"
                 
phone_sub = r"+7(\2)\3-\4-\5 \6\7"


# In[32]:


# TODO 1: выполните пункты 1-3 ДЗ
# ваш код
new_list = []
for item in contacts_list[1:]:
    data = ' '.join(item[:3]).split(' ')
    result = [data[0], data[1], data[2], item[3], item[4], re.sub(pattern, phone_sub, item[5]), item[6]]
    #print(result)
    new_list.append(result)

for contact in new_list:
    last_name = contact[0]
    first_name = contact[1]
    #print(first_name)
    for new_contact in new_list:
        new_last_name = new_contact[0]
        new_first_name = new_contact[1]
        if last_name == new_last_name and first_name == new_first_name: 
            if contact[2] == "": contact[2] = new_contact[2]
            if contact[3] == "": contact[3] = new_contact[3]
            if contact[4] == "": contact[4] = new_contact[4]
            if contact[5] == "": contact[5] = new_contact[5]
            if contact[6] == "": contact[6] = new_contact[6]
    
result_list = []
for i in new_list:
    if i not in result_list:
        result_list.append(i)

pprint(result_list)


# In[33]:


# TODO 2: сохраните получившиеся данные в другой файл
# код для записи файла в формате CSV
with open("D:/Python-developer/Python/RegEx/phonebook.csv", "w", encoding="utf-8") as f:
    datawriter = csv.writer(f, delimiter=',')
    # Вместо contacts_list подставьте свой список
    datawriter.writerows(result_list)

