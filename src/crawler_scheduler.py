from src.hyperlink_collector import  Hyperlink_Collector
import json
import boto3
from boto3.dynamodb.conditions import Attr
import datetime
from datetime import datetime

# Function to read the table AWS DynamoDb daily and get the URLs to crawl

def lambda_handler():
    # connect to dynamodb
    client = boto3.Session(region_name='eu-central-1',
                           aws_access_key_id='**************************',
                           aws_secret_access_key='**************************')
    table = client.resource('dynamodb').Table('seeds')

    # create string date for today
    today = datetime.now().date()
    str_today = today.strftime('%Y-%m-%d')
    print(str_today)
    # get all cities that should be crawled today
    response = table.scan(
        FilterExpression=Attr('next_schedule').eq(str_today)
    )

    for item in response['Items']:
        collector= Hyperlink_Collector(item['url'])
        collector.collect()

if __name__== "__main__":
    lambda_handler()
