import pandas
import re
from bs4 import BeautifulSoup
import requests

# read the csv file and get cities list:
df = pandas.read_csv('seed_gross_mittel_list.csv',sep=';',header=None,encoding='iso-8859-1')
seeds = df.iloc[:,[1]].values.tolist()

seed_link ={}

for seed in seeds:
    print('-----------------------------------------------------------',seed)
    r = requests.get('https://www.google.com/search?q={0}+amtsblatt'.format(str(seed[0])))
    print(r)
    data = r.text
    soup = BeautifulSoup(data,'lxml')
    raw = soup.find_all("div",class_='g',limit=10)
    raws_splitted = str(raw).split('?q=')
    cut_tails = []

    for i in raws_splitted:
        head,sep,tail=i.partition('">')

    remove_google_ad=[]
    for url in cut_tails[1:]:
        head,sep,tail = url.partition('&amp')
        remove_google_ad.append(head)
    #print(remove_google_ad)
    seed_link[str(seed[0])]= remove_google_ad

import csv

with open('test.csv', 'w') as f:
    for key in seed_link.keys():
        f.write("%s,%s\n"%(key,seed_link[key]))