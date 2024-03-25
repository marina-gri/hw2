import re
from pprint import pprint
import csv


# читаем адресную книгу в формате CSV в список contacts_list

with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)
pprint(contacts_list)

# TODO 1: выполните пункты 1-3 ДЗ
contacts_dict = {}
for item in contacts_list:
    full_name = " ".join(item[:3]).strip()
    last_first_name = " ".join(full_name.split()[:2])

    if last_first_name in contacts_dict:
        for i in range(len(item)):
            if i > 2:
                contacts_dict[last_first_name].append(item[i])
    else:
        if len(full_name.split()) == 3:
            contacts_dict[last_first_name] = [full_name.split()[2]]
            for i in range(len(item)):
                if i > 2:
                    contacts_dict[last_first_name].append(item[i])

    contacts_dict[last_first_name] = list(set(contacts_dict[last_first_name]))
    while "" in contacts_dict[last_first_name]:
        contacts_dict[last_first_name].remove("")
pprint(contacts_dict)

ptrn_surname_compiled = re.compile(r"[а-яёА-ЯЁ]+(вна|вич)")
ptrn_organization_compiled = re.compile(r"Минфин|ФНС")
ptrn_position_compited = re.compile(r"[А-ЯЁа-яёA-Za-z –]+отдел[А-ЯЁа-яёA-Za-z ]+")
ptrn_phone_compiled = re.compile(r"(\+?7|8?)\s?\(?(\d{3})\)?\s?-?(\d{3})\s?-?(\d{2})\s?-?(\d{2})\s?\(?(доб\.)?\s?(\d+)?\)?")
phone_sub = r"+7(\2)\3-\4-\5 \6\7"
ptrn_email_compiled = re.compile(r"[a-zA-Z0-9._-]+@[a-zA-Z_-]+[.][a-z]+")


result = [['lastname',
          'firstname',
          'surname',
          'organization',
          'position',
          'phone',
          'email']]
for key, value in contacts_dict.items():
    if key == "lastname firstname":
        pass
    else:
        value = str(value)
        key = key.split()
        surname = ptrn_surname_compiled.search(value).group()
        organization = ptrn_organization_compiled.search(value).group()
        phone = ptrn_phone_compiled.sub(phone_sub, ptrn_phone_compiled.search(value).group())
        email = ptrn_email_compiled.search(value).group() if ptrn_email_compiled.search(value) is not None else ""
        position = ptrn_position_compited.search(value).group() if ptrn_position_compited.search(value) is not None else ""

        result.append([key[0], key[1], surname, organization, position, phone, email])

pprint(result)

#TODO 2: сохраните получившиеся данные в другой файл
# код для записи файла в формате CSV
with open("phonebook_corrected.csv", "w", encoding="utf-8", newline='') as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(result)
