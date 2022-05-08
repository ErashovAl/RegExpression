import re
import csv

phone_clean_rx = re.compile('\D')

def clean_phone(phone):
    phone_clean = phone_clean_rx.sub('', phone)

    if len(phone_clean) == 0:
        return ''

    area = phone_clean[1:4]
    nums = (phone_clean[4:7], phone_clean[7:9], phone_clean[9:11])
    ext = ''
    
    if len(phone_clean) > 11:
        ext = phone_clean[11:]
        return f"+7({area}){nums[0]}-{nums[1]}-{nums[2]} доб.{ext}"

    return f"+7({area}){nums[0]}-{nums[1]}-{nums[2]}"

def merge_contact(a, b):
    
    res = a

    for i in range(len(a)):
        res[i] = a[i] or b[i]

    return res

def merge(contacts):
   
    duplicate_dict = {}

    for contact in contacts:
        full_name = f"{contact[0]} {contact[1]}"
        if full_name not in duplicate_dict:
            duplicate_dict[full_name] = contact
        else:
            duplicate_dict[full_name] = merge_contact(duplicate_dict[full_name], contact)
    

    return list(duplicate_dict.values())

path_to_file = ('phonebook_raw.csv')

with open(path_to_file, encoding='utf-8') as f:
    csv_rows = csv.reader(f, delimiter=',')
    raw_contacts = list(csv_rows)

    for rows in raw_contacts:
        rows[5] = clean_phone(rows[5])
        name_list = [rows[0], rows[1], rows[2]]
        joined_list = ' '.join(name_list).split()        
        if len(joined_list) == 2:
            rows[0], rows[1] = joined_list[0], joined_list[1]
        else:
            rows[0], rows[1], rows[2] = joined_list[0], joined_list[1], joined_list[2]   

    merge_list = merge(raw_contacts)

with open('phonebook.csv', 'wt', newline='', encoding='utf-8') as f:
    datawriter = csv.writer(f)
    datawriter.writerows(merge_list)