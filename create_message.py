from urllib.request import urlopen
from bs4 import BeautifulSoup
import config
import boto3
import botocore

#create the sqs client
sqs= boto3.client('sqs', config.CURRENT_REGION,config.AWS_CONFIG['AWS_SERVER_PUBLIC_KEY'],config.AWS_CONFIG['AWS_SERVER_SECRET_KEY'])

# create / open the SQS queue
queue = sqs.create_queue(QueueName = "")
print(queue)

# read and parse the planets HTML
url =''
html = urlopen(url)

#### HTML contents processing

context =''
sqs.send_message(QueueURL=queue["QueueUrl"],
                 MessageBody=context )

