from pprint import pprint
import csv
import re

# 1. Читаем исходный CSV-файл
with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

# 2. Регулярное выражение для телефонов
phone_pattern = re.compile(
    r"(\+7|8)\s*\(?(\d{3})\)?[\s-]*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})(\s*\(?(доб\.?)\s*(\d+)\)?)?"
)

# 3. Приводим ФИО и телефоны к нормальному виду
for contact in contacts_list[1:]:
    # --- ФИО ---
    fio = " ".join(contact[:3]).split()
    contact[0] = fio[0]
    contact[1] = fio[1] if len(fio) > 1 else ""
    contact[2] = fio[2] if len(fio) > 2 else ""

    # --- Телефон ---
    phone = contact[5]
    if phone:
        match = phone_pattern.search(phone)
        if match:
            phone_result = f"+7({match.group(2)}){match.group(3)}-{match.group(4)}-{match.group(5)}"
            if match.group(8):
                phone_result += f" доб.{match.group(8)}"
            contact[5] = phone_result

# 4. Объединяем дубликаты (по Фамилии и Имени)
contacts_dict = {}

for contact in contacts_list[1:]:
    key = (contact[0], contact[1])

    if key not in contacts_dict:
        contacts_dict[key] = contact
    else:
        existing = contacts_dict[key]
        for i in range(7):
            if existing[i] == "":
                existing[i] = contact[i]

# 5. Собираем финальный список
final_contacts = [contacts_list[0]]
final_contacts.extend(contacts_dict.values())

# 6. Записываем результат в новый CSV-файл
with open("phonebook.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f, delimiter=",")
    writer.writerows(final_contacts)

print("Файл phonebook.csv успешно создан")
