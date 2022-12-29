import pandas as pd

# https://www.freecodecamp.org/news/how-to-get-started-with-firebase-using-python/

keep = open('macula/word-features.txt','r').read().splitlines()

data= pd.read_csv('macula/macula-hebrew.tsv',sep='\t')

for name in keep:
    if name not in data.columns:
        print(name)