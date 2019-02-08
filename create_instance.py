
import boto3
import config

session = boto3.Session(region_name=config.CURRENT_REGION,
                        aws_access_key_id=config.AWS_CONFIG['AWS_SERVER_PUBLIC_KEY'],
                        aws_secret_access_key=config.AWS_CONFIG['AWS_SERVER_SECRET_KEY'])

client = session.resource('ec2')
#create a new ec2 instance
instances = client.create_instances(
     ImageId='ami-0bdf93799014acdc4',
     MinCount=1,
     MaxCount=2,
     InstanceType='t2.micro'
)

