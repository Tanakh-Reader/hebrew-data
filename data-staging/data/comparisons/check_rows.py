import csv
import pandas as pd


source_file_path = '/Users/sethhowell/Desktop/Hebrew-Literacy-App/hebrew-data/data-staging/data/comparisons/macula-to-etcbc-comparison.csv'

rows = []

with open(source_file_path, 'r') as csv_file:
    print("START")
    csv_rows = list( csv.reader(csv_file, delimiter=',') )
    streak = 0
    start = 0
    values = []
    for row_index, row in enumerate(csv_rows[1:]):
        if int(row[4]) > 3:
            if int(csv_rows[row_index-1][4]) < 3:
                start = row_index
            streak += 1
            values.append(row[4])
        else:
            if streak > 3:
                affixes = len([i for i in values if i == "4"])
                if affixes / len(values) < 0.8:
                    while start <= row_index:   
                        rows.append(csv_rows[start])
                        start += 1
                    rows.append([])
            streak = 0
            values = []

df = pd.DataFrame(rows, dtype=str)
df.to_csv("check_rows.txt", sep=',', encoding='utf-8', index=False)