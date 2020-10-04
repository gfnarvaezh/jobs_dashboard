import boto3
from datetime import datetime

today = datetime.today().strftime('%y%m%d')
client = boto3.client('dynamodb')

# Ads the idem to the table in DynamoDB

def add_to_table(identifier, value):
    response = client.update_item(
        TableName='personal_proyects',
        Key={
            'identifier': {'S':identifier},
            'sort_key': {'S': 'none'}
        },
        UpdateExpression="SET d" + today + " = :jobs",
        ExpressionAttributeValues={
            ':jobs': {'N': str(value)}
        }
    )
    return response