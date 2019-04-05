import boto3
import config

class BotoClient:
    def __init__(self,resource):
        self.Session = boto3.Session(region_name=config.CURRENT_REGION,
                        aws_access_key_id=config.AWS_CONFIG['AWS_SERVER_PUBLIC_KEY'],
                        aws_secret_access_key=config.AWS_CONFIG['AWS_SERVER_SECRET_KEY'])
        self.resource = resource


    def connect (self):
        return self.Session.resource(self.resource)

