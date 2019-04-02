from bs4 import BeautifulSoup
import requests
import csv
import json
import boto3
from src import config
from boltons.iterutils import remap

bundeslaender =['Baden-Württemberg',
                'Freistaat Bayern',
                'Berlin',
                'Brandenburg',
                'Bremen',
                'Hamburg',
                'Hessen',
                'Mecklenburg-Vorpommern',
                'Niedersachsen',
                'Nordrhein-Westfalen',
                'Rheinland-Pfalz',
                'Saarland',
                'Sachsen',
                'Sachsen-Anhalt',
                'Schleswig-Holstein',
                'Freistaat Thüringen']

r = requests.get('https://www.prospektverteilung-hamburg.de/?p=bundeslaender')
data = r.text
soup = BeautifulSoup(data,'lxml')
seed= 'https://www.prospektverteilung-hamburg.de/'
urls_list = []
with open('urls.csv', mode='r') as csv_file:
    csv_reader = csv.reader(csv_file)
    for row in csv_reader:
        urls_list.append(seed+str(row[0]))


id = 1
for i in urls_list:
    bundesland = {}
    bundesland["ID"] = str(id)
    bundesland["name"] = str(i.split('=')[-1])

    if str(i).find("=bayern") is not -1:
        pass
    elif str(i).find("=bremen")is not -1:
        bundesland['stadt']='bremen'
    elif str(i).find("=hamburg")is not -1:
        bundesland['stadt']='hamburg'
    elif str(i).find("=berlin") is not -1:
        bundesland['stadt']='berlin'
    else:
        r1 = requests.get(i)
        encoding = r1.encoding if 'charset' in r.headers.get('content-type', '').lower() else None
        soup1 = BeautifulSoup(r1.content,from_encoding=encoding, features='lxml')
        producers = soup1.find_all('div', class_='advert')
        landkreis_list =[]
        for producer in producers:
            root = producer.find_all("h3")
            for para in root:
                landkreis = {}
                landkreis["name"] = para.getText()
                dummytext= para.find_next("p")
                staedte_gemeinden =dummytext.find_next("p").getText()

                staedte = str(staedte_gemeinden).partition('Gemeinden:')[0].replace('Städte:','').replace('.','').replace('und',',')
                gemeinden = str(staedte_gemeinden).partition('Gemeinden:')[2].replace('.','').replace('und',',')

                if len(gemeinden.split(','))>0:
                    landkreis["gemeinden"]= gemeinden.split(',')
                if len(staedte.split(',')) != 0:
                    landkreis["staedte"]=staedte.split(',')
                landkreis_list.append(landkreis)
            if len(landkreis)>0:
                bundesland["landkreise"] = landkreis_list
    id = id +1

    ### Remove emoty fields before upload in DynamoDb
    drop_falsey = lambda path, key, value: bool(value)
    clean = remap(bundesland, visit=drop_falsey)
    output = json.dumps(clean,ensure_ascii=False).encode("utf-8")
    session = boto3.Session(region_name=config.CURRENT_REGION,
                            aws_access_key_id=config.AWS_CONFIG['AWS_SERVER_PUBLIC_KEY'],
                            aws_secret_access_key=config.AWS_CONFIG['AWS_SERVER_SECRET_KEY'])
    dynamodb = session.resource('dynamodb').Table('geo')
    res = dynamodb.put_item(Item=json.loads(output))