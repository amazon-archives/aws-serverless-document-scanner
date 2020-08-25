import os
import json, decimal
import boto3
from boto3.dynamodb.conditions import Key, Attr

tableName = os.environ.get('PAGES_TABLE_NAME')

def handler(event, context):
  client = boto3.resource('dynamodb')

  table = client.Table(tableName)

  print(table.table_status)
  print(event)

  username = event['requestContext']['authorizer']['claims']['cognito:username']
  project = username + '/' + event['pathParameters']['project']

  res = table.scan(FilterExpression=Key('project').eq(project))

  data = res['Items']

  while 'LastEvaluatedKey' in res:
      res = table.scan(ExclusiveStartKey=res['LastEvaluatedKey'])
      data.extend(res['Items'])

  body = {
    "page_count": len(data)
  }

  response = {
    "statusCode": 200,
    "body": json.dumps(body),
    "headers": {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "*"
    }
  }

  print(response)
  return response