from googlesearch import search
import boto3
import json
from boto3.dynamodb.conditions import Key,Attr
import config

geo =[]
seeds=[]

session = boto3.Session(region_name=config.CURRENT_REGION,
                        aws_access_key_id=config.AWS_CONFIG['AWS_SERVER_PUBLIC_KEY'],
                        aws_secret_access_key=config.AWS_CONFIG['AWS_SERVER_SECRET_KEY'])
table = session.resource('dynamodb').Table('geo')
response = table.scan()
for i in response['Items']:
    for landkreis in i['landkreis']:
        for i in landkreis['gemeind']:
            geo.append(i)
        for i in landkreis['stadt']:
            geo.append(i)
print(geo)

for i in geo:
    for url in search(str(i)+'Amtsblatt', stop=1):
        seeds.append(str(url))
print(seeds)
