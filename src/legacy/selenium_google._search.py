from selenium import webdriver
from time import  sleep
import urllib.parse
import re
import pandas
import json
import boto3

# open the dynamodb session
session = boto3.Session(region_name='eu-central-1',
                        aws_access_key_id='AKIAJHK4UKVNUFHNWRVQ',
                        aws_secret_access_key='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')
# read the csv file and get cities list:
df = pandas.read_csv('seed_gross_mittel_list.csv',sep=';',header=None,encoding='iso-8859-1')

for index,row in df.iterrows():
    browser = webdriver.Chrome()
    browser.get('http://www.google.de')
    #WebDriverWait(browser,10).until(EC.presence_of_all_elements_located((By.ID,"gbqfq")))

    search = browser.find_element_by_name('q')
    s =' '
    search.send_keys(str(row[1])+' Amtsblatt')
    search.submit()
    sleep(1)
    links = browser.find_elements_by_class_name('r')
    urls=[]
    for link in links:
        a = link.find_element_by_tag_name('a')
        url = urllib.parse.unquote(a.get_attribute('href'))
        url = re.sub("^.*?(?:url\?q=)(.*?)&sa.*",r"\1",url,0,re.IGNORECASE)
        urls.append(url)
    browser.quit()

    #write the data to dynamodb
    obj ={}
    obj['ID']= str(row[0])
    obj['name'] = str(row[1])
    obj['url']= urls
    output = json.dumps(obj, ensure_ascii=False).encode("utf-8")
    dynamodb = session.resource('dynamodb').Table('urls_cities')
    res = dynamodb.put_item(Item=json.loads(output))
    print(row[1],'\t has been processed')