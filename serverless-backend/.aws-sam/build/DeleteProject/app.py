import os
import json
import boto3
from boto3.dynamodb.conditions import Key, Attr

projectsTableName = os.environ.get('PROJECTS_TABLE_NAME')
pagesTableName = os.environ.get('PAGES_TABLE_NAME')
bucketName = os.environ.get('BUCKET_NAME')

s3 = boto3.resource('s3')
bucket = s3.Bucket(bucketName)

client = boto3.resource('dynamodb')
pagesTable = client.Table(pagesTableName)
projectsTable = client.Table(projectsTableName)

def handler(event, context):
  print(projectsTable.table_status)
  print(pagesTable.table_status)
  print(event)

  username = event['requestContext']['authorizer']['claims']['cognito:username']
  body = json.loads(event['body'])
  projectName = body['name']
  projectKey = username + '/' + projectName 
  folderPrefix = 'private/' + body['identityId'] + '/' + projectKey
  
  projectsTable.delete_item(Key= {
    'username': username,
    'project_name': projectName,
    })


  scan = pagesTable.scan(FilterExpression=Key('project').eq(projectKey))
  with pagesTable.batch_writer() as batch:
    for each in scan['Items']:
      batch.delete_item(
        Key={
          'project': each['project'],
          'page': each['page']
        }
  )

  bucket.objects.filter(Prefix=folderPrefix).delete()

  response = {
    "statusCode": 200,
    "headers": {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "*"
    }
  }
  return response