from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import re
import pandas as pd
from tabulate import tabulate
import os
import lxml
import googleapiclient
import requests
from pathlib import  Path
import urllib.request
# launch url
url = "https://www.nuernberg.de/internet/pr/amtsblatt_2018.html"

# create a new Firefox session
binary =r'C:\Program Files\chromedriver.exe'
driver = webdriver.Chrome(binary)
driver.implicitly_wait(30)
driver.get(url)
#r = requests.get("")
#get the list of the download attribute
links_list = driver.find_elements_by_partial_link_text("Amtsblatt der Stadt")
i =0
for link in links_list:
    filename= link.text+'.pdf'
    # request for the pdf file
    url =  link.get_attribute('href')
    r= requests.get(url)
    with open('test'+'_'+str(i)+'.pdf', 'wb') as fd:
         fd.write(r.content)
    i= i+1
driver.close()