from selenium import webdriver
import boto3
import requests
import config

# launch url
url = "https://www.nuernberg.de/internet/pr/amtsblatt_2018.html"

client = boto3.client('s3')

# create a new Firefox session
driver = webdriver.Chrome()
driver.implicitly_wait(30)
driver.get(url)

#get the list of the download attribute
links_list = driver.find_elements_by_partial_link_text("Amtsblatt der Stadt")
i = 0
for link in links_list:
    filename= link.text+'.pdf'
    # request for the pdf file
    url = link.get_attribute('href')
    r = requests.get(url)
    session = boto3.Session(region_name=config.CURRENT_REGION,
                            aws_access_key_id=config.AWS_CONFIG['AWS_SERVER_PUBLIC_KEY'],
                            aws_secret_access_key=config.AWS_CONFIG['AWS_SERVER_SECRET_KEY'])
    client = session.resource('s3')
    key = 'text1.txt'
    res = client.Bucket('amtsblatt').put_object(Key=filename, Body=r.content)
    i= i+1
driver.close()
