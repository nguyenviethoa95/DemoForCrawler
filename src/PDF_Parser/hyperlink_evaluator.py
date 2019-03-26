import requests
from pytesseract import pytesseract
import boto3
import uuid
import datetime

def create_S3_connection():
    client = boto3.client('s3', region_name='eu-central-1',
                          aws_access_key_id='AKIAJHK4UKVNUFHNWRVQ',
                          aws_secret_access_key='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')
    return client

def create_dynamodb_connection():
    client = boto3.client('dynamodb', region_name='eu-central-1',
                          aws_access_key_id='AKIAJHK4UKVNUFHNWRVQ',
                          aws_secret_access_key='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')
    return client

try:
    dynamodb_client = create_S3_connection()
except Exception as e:
    # Workflow(e,'')

def is_PDFFile(url):
    """
    Checking if document is a PDF File
    """
    h = requests.head(url, allow_redirects = True)
    header= h.headers
    content_type= header.get('content-type')
    if 'pdf' in content_type.lower():
        return True
    return False

def get_pdf(url):
    try:
        req = requests.get(url,stream =True)
        return req
    except Exception as e:
        return e

def put_object (client, object):
    try:
        client.put_object(Body = object,bucket='demo-crawler',Key='')
    except Exception as e:
        return e

#class Workflow_Record(end_point,workflowname,exception,message):

def insert_Workflow_Record(*args):
    #for record in args:

def mark_visited(id):
    dynamodb_client.Table('urls_list').update_item(
        Key={
            'uuid': str(id)
        },
        UpdateExpression="SET visited = :var1",
        ExpressionAttributeValues={
            ':var1': True),
        },
    )
def mark_downloaded(id):
    dynamodb_client.Table('urls_list').update_item(
        Key={
            'uuid': str(id)
        },
        UpdateExpression="SET downloaded = :var1",
        ExpressionAttributeValues={
            ':var1': True,
        },
    )

def mark_invalid(id):
    dynamodb_client.Table('urls_list').update_item(
        Key={
            'ID': str(id)
        },
        UpdateExpression="SET valid = :var1",
        ExpressionAttributeValues={
            ':var1': False,
        },
    )

def get_random_link_to_visit():
    link = dynamodb_client.Table('urls_list').query(
        # Insert query here
    )
    return None if link is None else link

def visit(url):
    id = uuid.uuid5(url)
    dynamodb_client.Table('urls_list').put_item(
        Item={}
    )
    mark_visited(id)
    if is_PDFFile(url) is not True:
        mark_invalid(url)


if __name__=="__main__":
    #print(is_PDFFile('https://www.fuerth.de/DownloadCount.aspx?raid=72006&docid=8605&rn=13f8f417-4c6e-4069-8d10-a5e7b7c8fa2e"'))
    urls=[]
    workflows_result=[]
    try:
        s3_client = create_S3_connection()
    except Exception as e:
        # Workflow(e,'hyperlink_evaluator')



    for url in urls:
       visit(url)
    workflow_tbl = dynamodb_client.Table('Workflow')
   # Write_Workflow(workflow_tbl,workflows_result)