import os
import json
import boto3

tableName = os.environ.get('PROJECTS_TABLE_NAME')

def handler(event, context):
  client = boto3.resource('dynamodb')

  table = client.Table(tableName)

  print(table.table_status)
  print(event)

  user_data = event['requestContext']['authorizer']['claims']
  timestamp = event['requestContext']['requestTimeEpoch']
  body = json.loads(event['body'])

  table.put_item(Item= {
    'username': user_data['cognito:username'],
    'timestamp': timestamp, 
    'project_name': body['name']
    })

  response = {
    "statusCode": 200,
    "body": "hi",
    "headers": {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "*"
    }
  }
  return response