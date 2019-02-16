import boto3
import config

#boto3.setup_default_session('s3',profile_name='boto3user')
session = boto3.Session(region_name=config.CURRENT_REGION,
                        aws_access_key_id=config.AWS_CONFIG['AWS_SERVER_PUBLIC_KEY'],
                        aws_secret_access_key=config.AWS_CONFIG['AWS_SERVER_SECRET_KEY'])
client=session.resource('s3')
key = 'text1.txt'
res = client.Bucket('amtsblatt').put_object(Key=key,Body=r'C:\Users\Nguyen Viet Hoa\Desktop\testfile.txt')
print(res)