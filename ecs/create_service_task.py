import boto3
import config

# Credentials & Region
access_key = config.AWS_CONFIG['AWS_SERVER_PUBLIC_KEY']
secret_key = config.AWS_CONFIG['AWS_SERVER_SECRET_KEY']
region =config.CURRENT_REGION

# ECS Details
cluster_name = "BotoCluster"
service_name ="service_hello_world"
task_name ="hello_world"

# Let's user Amazon ECS
ecs_client = boto3.client(
    'ecs',
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
    region_name=region
)

# Let's use Amazon EC2
ec2_client =  boto3.client(
    'ec2',
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
    region_name=region
)

def launch_ecs_example():
    response = ecs_client.create_cluster(
        cluster_name=cluster_name
    )

    print(response)

response = ec2_client.run_instancees(

)