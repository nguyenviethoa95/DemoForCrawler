from bs4 import BeautifulSoup
import requests
from src.baseclass import BotoClient
import uuid
from urllib.parse import urljoin
from boto3.dynamodb.conditions import Attr

class Hyperlink_Collector:
    def __init__(self,parent_url):
        self.client = BotoClient.BotoClient('dynamodb').connect()
        self.parent_url = parent_url

    def getPage(self):
        try:
            req = requests.get(self.parent_url)
        except requests.exceptions.RequestException:
            return None
        return BeautifulSoup(req.text,'lxml')

    def safeGet(self,pageObj,selector):
        pass

    def isAbsoluteLink(self, link):
        if str(link).startswith("http://") or str(link).startswith("https://"):
            return True
        return False

    def resolveRelativeURL(self,parent_url,url):
        return urljoin(parent_url,url)

    def insert_hyperlink(self,url,link_text):
        # Assign a uuid for the pdf document
        id = uuid.uuid4()
        self.client.Table('urls_list').put_item(
           Item= {
                "downloaded": False,
                "downloaded_on": "None",
                "full_url": str(url),
                "parent_url":str(self.parent_url),
                "link_text": str(link_text),
                "uuid": str(id),
                "valid": True,
                "visited": False,
                "visited_on": "None",
                "downloaded_tries_number":0
            }
        )

    def isURLDupilcate(self, url):
        table= self.client.Table('url_list_bernburg')
        res = table.scan(
            FilterExpression=Attr('full_url').eq(url),
        )
        return True if len(res['Items'])!=0 else False

    def is_PDFFile(self,url):
        """
        Checking if document is a PDF File
        """
        h = requests.head(url, allow_redirects=True)
        header = h.headers
        content_type = header.get('content-type')
        if 'pdf' in content_type.lower():
            return True
        if 'pdf' in url:
            return True
        return False

    def collect(self):
        """
        Searches a given website for all links related to Amtsblatt and records all pages found
        """
        soup = self.getPage()
        for link in soup.findAll('a'):
            text = str(link.getText().strip())
            href = str(link.get('href'))

            if self.isAbsoluteLink(href) is not True:
                href = self.resolveRelativeURL(self.parent_url,href)
                print(href)
            #f self.is_PDFFile(href):
                #if 'amtsblatt' in text.lower() or 'amtsblaetter' in text.lower() or 'pdf' in text.lower():
            if 'pdf' in href and self.isURLDupilcate(href) is False:
               self.insert_hyperlink(href, text)

def main(url):
    collector = Hyperlink_Collector(url)
    collector.collect()

if __name__=="__main__":
    url = 'https://www.bernburg.de/de/amtsblaetter-2019.html'
    main(url)
