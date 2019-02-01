import boto3
import config

session = boto3.Session(region_name=config.CURRENT_REGION,
                        aws_access_key_id=config.AWS_CONFIG['AWS_SERVER_PUBLIC_KEY'],
                        aws_secret_access_key=config.AWS_CONFIG['AWS_SERVER_SECRET_KEY'])
conexao = session.client('rds',region_name=config.CURRENT_REGION)

try:
    dbs = conexao.describe_db_instances()
    for db in dbs['DBInstances']:
        print(db['MasterUsername'], db['Endpoint']['Address'],db['Endpoint']['Port'],db['DBInstanceStatus'])
        print(db)
        hostname= db['Endpoint']['Address']
except Exception as e:
    print('Exception'+e)

import pymysql

conn = pymysql.connect(host=hostname, port=3306, user='master', password ='tha'
                                                                          'ian8355',db='webcrawler',connect_timeout=5)

cur = conn.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS numbers (url varchar(256), number integer, PRIMARY KEY (url, number))")

print(cur.description)

print()

for row in cur:
    print(row)

cur.close()
conn.close()