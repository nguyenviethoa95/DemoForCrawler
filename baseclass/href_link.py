import requests
from baseclass import BotoClient,BotoResource
import uuid

class href_link:
    def __init__(self, url,title ):
        self.url =url
        self.title=title

    def contain_keyword (self):
        if self.url.find('amtsblatt') != -1 or self.title.find('amtsblatt') != -1:
            return True
        else:
            return False

    def isPDFFile (self):
        if self.url.find('.pdf') != -1:
            return True
        else:
            return False

    def markInvalid (self):
        ''' Write into db invalid'''

    def Retrieve(self,bucket):
        if self.isPDFFile() == True:
            if self.contain_keyword() == True:
                req = requests.get(self.url, stream=True)
                client = BotoClient(BotoResource.BotoResource.S3.value).connect()


        else:
            self.markInvalid()
