import csv
raw_data_url = []
raw_data_titel = []
with open('details.csv', 'r') as file_name:
    reader = csv.reader(file_name)
    for row in reader:
        raw_data_url.append(row[1])
        raw_data_titel.append(row[0])
        print(row[1])
for i, x in enumerate(raw_data_url):
    if x is not '':
        raw_data_url[i] = 'https://www.zoopla.co.uk'+x
        print(i,' details are many ', x, ' but details are here', raw_data_url[i])
with open('details.csv','a') as file_names:
    writer = csv.writer(file_names)
    for x, y in zip(raw_data_titel,raw_data_url):
        writer.writerow([x, y])