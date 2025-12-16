from pprint import pprint
import csv
import re

with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

phone_pattern = re.compile(
    r"(\+7|8)\s*\(?(\d{3})\)?[\s-]*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})(\s*\(?(доб\.?)\s*(\d+)\)?)?"
)

for contact in contacts_list[1:]:
    fio = " ".join(contact[:3]).split()
    contact[0] = fio[0]
    contact[1] = fio[1] if len(fio) > 1 else ""
    contact[2] = fio[2] if len(fio) > 2 else ""

    phone = contact[5]
    if phone:
        result = phone_pattern.search(phone)
        if result:
            formatted_phone = f"+7({result.group(2)}){result.group(3)}-{result.group(4)}-{result.group(5)}"
            if result.group(8):
                formatted_phone += f" доб.{result.group(8)}"
            contact[5] = formatted_phone

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

final_contacts = [contacts_list[0]]
final_contacts.extend(contacts_dict.values())

with open("phonebook.csv", "w", encoding="utf-8") as f:
    writer = csv.writer(f, delimiter=",")
    writer.writerows(final_contacts)
