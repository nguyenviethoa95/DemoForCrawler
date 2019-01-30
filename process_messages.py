import boto3
import botocore

import requests
from bs4 import BeautifulSoup
import config

print('Starting')

# create sqs client
sqs = boto3.client('sqs',
                   config.CURRENT_REGION,
                   config.AWS_CONFIG['AWS_SERVER_PUBLIC_KEY'],
                   config.AWS_CONFIG['AWS_SERVER_SECRET_KEY']
)

# create/open the SQS queue

queue = sqs.create_queue(QueueName ="")
queue_url = queue['QueueUrl']
print("Opened queue %s"%queue_url)

while True:
    print('Attempting to receive messages')
    response = sqs.receive_message(QueueUrl= queue_url,
                                   MaxNumberOfMessage = 1,
                                   WaitTimeSeconds = 1)
    if not 'Messages' in response:
        print('No messages')
        continue

    message = response['Messages'][0]
    url = message['Body']

    # parse the page
    html = requests.get(url)
    bsobj = BeautifulSoup(html.text,'lxml')

    # delete the message from the queue
    sqs.delete_message(
        QueueUrl = queue_url,

    )