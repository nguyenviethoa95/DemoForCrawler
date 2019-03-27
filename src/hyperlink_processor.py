import requests
from datetime import datetime
from boto3.dynamodb.conditions import Attr
from src.baseclass import BotoClient


# def create_S3_connection():
#     client = boto3.resource('s3', region_name='eu-central-1',
#                           aws_access_key_id='AKIAJHK4UKVNUFHNWRVQ',
#                           aws_secret_access_key='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')
#     return client
#
# def create_dynamodb_connection():
#     client = boto3.resource('dynamodb', region_name='eu-central-1',
#                           aws_access_key_id='AKIAJHK4UKVNUFHNWRVQ',
#                           aws_secret_access_key='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')
#     return client

def get_pdf(url):
    try:
        req = requests.get(url,stream =True)
        return req.content
    except Exception as e:
        return e

def put_object (id, content):
    try:
        s3_client.Object('demo-crawler',str(id)+'.pdf').put(Body=content)
    except Exception as e:
        return e

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

def insert_Workflow_Record(*args):
    pass

def mark_visited(id):
    dynamodb_client.Table('urls_list').update_item(
        Key={
            'uuid': str(id)
        },
        UpdateExpression="SET visited = :var1, visited_on= :var2",
        ExpressionAttributeValues={
            ':var1': True,
            ':var2': str(datetime.utcnow().isoformat())
        }
    )
def mark_downloaded(id):
    dynamodb_client.Table('urls_list').update_item(
        Key={
            'uuid': str(id)
        },
        UpdateExpression="SET downloaded = :var1, downloaded_on = :var2",
        ExpressionAttributeValues={
            ':var1': True,
            ':var2': str(datetime.utcnow().isoformat())
        },
    )

def mark_invalid(id):
    dynamodb_client.Table('urls_list').update_item(
        Key={
            'uuid': str(id)
        },
        UpdateExpression="SET valid = :var1",
        ExpressionAttributeValues={
            ':var1': True,
        },
    )

def get_random_link_to_visit():
    table = dynamodb_client.Table('urls_list')
    response = table.scan(
        FilterExpression= Attr('visited').eq(False),
    )
    result = len(response['Items'])
    return (None,None) if result==0 else (response['Items'][0]['uuid'],response['Items'][0]['full_url'])

def visit(id,url):

    mark_visited(id)
    if is_PDFFile(url) is not True:
        mark_invalid(url)
    content=get_pdf(url)
    put_object(id,content)
    mark_downloaded(id)


if __name__=="__main__":
    try:
        dynamodb_client = BotoClient.BotoClient('dynamodb').connect()
    except Exception as e:
        pass

    try:
        s3_client = BotoClient.BotoClient('s3').connect()
    except Exception as e:
        pass

    id_to_visit, url_to_visit = get_random_link_to_visit()
    while url_to_visit is not None:
        visit(id_to_visit,url_to_visit)
        id_to_visit,url_to_visit= get_random_link_to_visit()