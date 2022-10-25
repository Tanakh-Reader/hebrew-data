import csv

items = {}
file = '/Users/sethhowell/Desktop/Hebrew-Literacy-App/hebrew-data/data-staging/sources/Clear-Bible/macula-hebrew/TSV/macula-hebrew.tsv'
with open(file, 'r') as csvfile:
    datareader = csv.reader(csvfile, delimiter="\t")
    for row in datareader:
        if row[0].endswith('ה'):
            translit = row[4] 
            if translit not in items:
                items[translit] = [row[3]]
            else:
                if row[3] != '':
                    items[translit].append(row[3])

print(items)