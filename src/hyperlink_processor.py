import requests
from datetime import datetime
from boto3.dynamodb.conditions import Attr
from src.baseclass import BotoClient

class Hyperlink_Processor:
    def __init__(self,s3_client,dynamodb_client):
        self.dynamodb_client=dynamodb_client
        self.s3_client=s3_client

    def get_pdf(self,url):
        try:
            req = requests.get(url,stream =True)
            return req.content
        except Exception as e:
            return e

    def put_object (self,id, content):
        try:
            self.s3_client.Object('demo-crawler',str(id)+'.pdf').put(Body=content)
        except Exception as e:
            return e

    def is_PDFFile(self,url):
        """
        Checking if document is a PDF File
        """
        h = requests.head(url, allow_redirects = True)
        header= h.headers
        content_type= header.get('content-type')
        if 'pdf' in content_type.lower():
            return True
        return False

    def insert_Workflow_Record(*args):
        pass

    def mark_visited(self,id):
        self.dynamodb_client.Table('urls_list').update_item(
            Key={
                'uuid': str(id)
            },
            UpdateExpression="SET visited = :var1, visited_on= :var2",
            ExpressionAttributeValues={
                ':var1': True,
                ':var2': str(datetime.utcnow().isoformat())
            }
        )

    def mark_downloaded(self,id):
        self.dynamodb_client.Table('urls_list').update_item(
            Key={
                'uuid': str(id)
            },
            UpdateExpression="SET downloaded = :var1, downloaded_on = :var2",
            ExpressionAttributeValues={
                ':var1': True,
                ':var2': str(datetime.utcnow().isoformat())
            },
        )

    def mark_invalid(self,id):
        self.dynamodb_client.Table('urls_list').update_item(
            Key={
                'uuid': str(id)
            },
            UpdateExpression="SET valid = :var1",
            ExpressionAttributeValues={
                ':var1': False,
            },
        )

    def get_random_link_to_visit(self):
        table = self.dynamodb_client.Table('urls_list')
        response = table.scan(
            FilterExpression= Attr('visited').eq(False),
        )
        result = len(response['Items'])
        return (None,None) if result==0 else (response['Items'][0]['uuid'],response['Items'][0]['full_url'])


    def visit(self,id,url):

        self.mark_visited(id)
        if self.is_PDFFile(url) is not True:
            self.mark_invalid(url)
        content=self.get_pdf(url)
        self.put_object(id,content)
        self.mark_downloaded(id)

def main():
    try:
        dynamodb_client = BotoClient.BotoClient('dynamodb').connect()
    except Exception as e:
        pass

    try:
        s3_client = BotoClient.BotoClient('s3').connect()
    except Exception as e:
        pass

    processor= Hyperlink_Processor(s3_client,dynamodb_client)
    id_to_visit, url_to_visit = processor.get_random_link_to_visit()
    while url_to_visit is not None:
        processor.visit(id_to_visit,url_to_visit)
        id_to_visit,url_to_visit= processor.get_random_link_to_visit()

if __name__=="__main__":
    main()