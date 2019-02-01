from googlesearch import search
import pandas
import re

# read the csv file and get cities list:
df = pandas.read_csv('seeds_gross_mittel_staedte.csv',sep=';',header=None,encoding='iso-8859-1')
seeds = df.iloc[:,[1]].values.tolist()
seed_link ={}
for seed in seeds:
    name = str(seed[0]).replace('(*)','').replace(' ','')
    query = re.sub(re.compile("\d"),'',name) + '\t Amtsblatt'

    urls =[]
    for url in search(query, stop=10):
        urls.append(str(url))
    seed_link[str(name)] = urls
print(seed_link)




