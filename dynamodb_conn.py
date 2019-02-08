# import boto3
# import config
# import json
#
# session = boto3.Session(region_name=config.CURRENT_REGION,
#                         aws_access_key_id=config.AWS_CONFIG['AWS_SERVER_PUBLIC_KEY'],
#                         aws_secret_access_key=config.AWS_CONFIG['AWS_SERVER_SECRET_KEY'])
# dynamodb = session.resource('dynamodb').Table('geo')
#
# res = dynamodb.put_item(
#     Item = dict
# )

from scrapy_spiders import url_spiders

spider = url_spiders.URL_Spider()
print(spider)