import csv

items = {}
file = '/Users/sethhowell/Desktop/Hebrew-Literacy-App/hebrew-data/data-staging/data/Clear-Bible/macula-hebrew-unformatted.tsv'
with open(file, 'r') as csvfile:
    datareader = csv.reader(csvfile, delimiter="\t")
    for row in datareader:
        if row[0].endswith('ה'):
            text = row[3] 
            if text not in items:
                items[text] = 1
            else:
                items[text] = items[text] + 1

print(items)