import boto3
import os

AWS_ACCESS_KEY = os.environ.get('NEURALPIT_AWS_ACCESS_KEY','')
AWS_SECRET_KEY = os.environ.get('NEURALPIT_AWS_SECRET_KEY','')

if AWS_ACCESS_KEY and AWS_SECRET_KEY:
    dynamodb = boto3.resource('dynamodb',
        region_name='ap-southeast-2',
        aws_access_key_id=AWS_ACCESS_KEY ,
        aws_secret_access_key=AWS_SECRET_KEY)
    s3 =  boto3.client('s3',
        aws_access_key_id=AWS_ACCESS_KEY ,
        aws_secret_access_key=AWS_SECRET_KEY)
    firehouse = boto3.client('firehose',
        region_name='ap-southeast-2',
        aws_access_key_id=AWS_ACCESS_KEY ,
        aws_secret_access_key=AWS_SECRET_KEY)
    ssm =  boto3.client('ssm',
        aws_access_key_id=AWS_ACCESS_KEY ,
        aws_secret_access_key=AWS_SECRET_KEY)
else:
    dynamodb = boto3.resource('dynamodb',region_name='ap-southeast-2')
    s3 =  boto3.client('s3')
    firehouse = boto3.client('firehose',region_name='ap-southeast-2')
    ssm = boto3.client('ssm')

