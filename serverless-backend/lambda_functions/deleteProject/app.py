# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.

# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

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