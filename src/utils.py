import hashlib
from src.baseclass import BotoClient
from bs4 import BeautifulSoup as bs
import requests

class websiteHasher:

    def __init__(self,url_id,url_to_hash):
        self.url_id = url_id
        self.url_to_hash = url_to_hash

    def generateHash(self):
        cleanedHTML = HTMLSelector(requests.get(self.url_to_hash).text).selectText()
        return hashlib.sha224(cleanedHTML).hexdigest()

    def getLastHash(self):
        conn = BotoClient.BotoClient('dynamodb').connect()
        table = conn.Table('seeds')
        res = table.get_item(
            Key={
                'ID': self.url_id
            }
        )
        return res['Items'][0]['lastHashValue']

    def updateHash(self,new_hash_value):
        conn = BotoClient.BotoClient('dynamodb').connect()
        table = conn.Table('seeds')
        table.update_item(
            Key={
                'ID': str(self.url_id)
            },
            UpdateExpression="SET lastHashValue = :var1",
            ExpressionAttributeValues={
                ':var1': new_hash_value
            }
        )

    def compareHash(self):
        lastHashValue = self.getLastHash()
        currentHashValue = self.generateHash()
        if lastHashValue != currentHashValue:
            self.updateHash(currentHashValue)


class HTMLSelector:
    def __init__(self,html):
        self.html = html

    ''''Select only the javascript and styles in the html document'''
    def selectJavascript(self):
        soup = bs(self.html,'lxml')
        return [x.extract() for x in soup.findAll(['script','style'])]

    def selectText(self):
        soup = bs(self.html,'lxml')
        for x in soup.findAll(['script','style']):
            x.decompose()
        text = soup.get_text()
        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
        # encode text
        return text.encode('utf-8')

class DynamoDBUtils:

    def __init__(self,tableName):
        self.tableName= tableName
        self.conn = BotoClient.BotoClient('dynamodb').connect()
        self.table = self.conn.Table(self.tableName)

    def getallItemsID(self):
        res = self.table.scan()
        id_list = [item['ID'] for item in res['Items']]
        return id_list

    def getallItemsIDandURL(self):
        res = self.table.scan()
        id_list = [(item['ID'],item['url']) for item in res['Items']]
        return id_list

if __name__ =="__main__":
    utils = DynamoDBUtils('seeds')
    id_list = utils.getallItemsIDandURL()

    for id,url in id_list:
        hasher = websiteHasher(id,url)
        hashValue = hasher.generateHash()
        hasher.updateHash(hashValue)

