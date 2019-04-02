import requests
from bs4 import BeautifulSoup

class CookiesSetter:
    def __init__(self):
        self.session = None
        self.headers=None
        self.url = None
        self.request= None

    def setCookies (self,url):
        self.session= requests.Session()
        self.headers={
            "User-Agent":"",
            "Accept":""
        }
        self.url = url
        self.request=self.session.get(url,headers= self.headers)

