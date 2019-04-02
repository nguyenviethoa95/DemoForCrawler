from src.baseclass import BotoClient
from boto3.dynamodb.conditions import Attr

client = BotoClient.BotoClient('dynamodb').connect()

table = client.Table('urls_list')

def urls_list_table_reset():
    response = table.scan(
        FilterExpression=Attr('downloaded').eq(True)
    )

    for item in response['Items']:
        table.update_item(
            Key={
                'uuid': str(item['uuid'])
            },
            UpdateExpression="SET visited = :var1,"
                             " visited_on= :var2,"
                             "downloaded = :var3,"
                             "downloaded_on = :var4",
            ExpressionAttributeValues={
                ':var1': False,
                ':var2': 'None',
                ':var3': False,
                ':var4': 'None'
            })

def remove_attribute():
    table= client.Table('urls_list')
    res=table.scan()
    data= res['Items']
    while 'LastEvaluatedKey' in res:
        res =table.scan(ExclusiveStartKey=res['LastEvaluatedKey'])
        data.update(res['Item'])

    for item in data:
        table.update_item(
            Key={
                'uuid': str(item['uuid'])
            },
            UpdateExpression="REMOVE visisted_on",
        )

if __name__ == "__main__":
    import time
    # from datetime import datetime
    # now = datetime.now().date()
    # print(now.strftime('%Y-%m-%d'))



