import json
import boto3

def get_identifier(event):
    print(event)
    language = event['language']
    country = event['country']
    platform = event['platform']
    category = event['category']
    identifier = language + '.' + platform + '.' + country + '.' + category
    print(identifier)
    return identifier

def get_jobs_data(identifier):
    client = boto3.client('dynamodb')
    response = client.get_item(
            TableName='personal_proyects',
            Key = {'identifier': {'S': identifier}, 'sort_key': {'S': 'none'}}
        )
    return response

def clean_response_item(item):
    output = item.copy()
    del output['identifier']
    del output['sort_key']
    for key in output:
        output[key] = output[key]['N']
    
    return output

def lambda_handler(event, context):
    identifier = get_identifier(event)
    response = get_jobs_data(identifier)
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        if 'Item' in response.keys():
            item = clean_response_item(response['Item'])
            json_response = {
                'HTTPStatusCode': 200,
                'data': item
            }
        else:
             json_response = {
                'HTTPStatusCode': 404,
                'data': 'Item not found'
            }
    else:
        json_response = {
                'tatusCode': response['ResponseMetadata']['HTTPStatusCode'],
                'data': 'Problem in the table',
            }


    return json_response