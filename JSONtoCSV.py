import json
import csv


with open("files/list.json", 'r', encoding='utf-8') as file:
    data = json.load(file)

top_500 = sorted(data, key = lambda x: x['position'])[:500]

with open('top_500.csv', 'w', newline="", encoding='utf-8') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=top_500[0].keys())
    writer.writeheader()
    writer.writerows(top_500)