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
import json, decimal
import boto3
import urllib.parse
from boto3.dynamodb.conditions import Key, Attr

client = boto3.resource('dynamodb')
textract = boto3.client('textract')

tableName = os.environ.get('PAGES_TABLE_NAME')

def handler(event, context):

  table = client.Table(tableName)

  print(table.table_status)
 
  key = urllib.parse.unquote(event['Records'][0]['s3']['object']['key'])
  bucket = event['Records'][0]['s3']['bucket']['name']
  project = key.split('/')[3]
  page = key.split('/')[4].split('.')[0]
  user = key.split('/')[2]
  
  response = textract.detect_document_text(
    Document={
        'S3Object': {
            'Bucket': bucket,
            'Name': key
        }
    })
    
  fullText = ""
  
  for item in response["Blocks"]:
    if item["BlockType"] == "LINE":
        fullText = fullText + item["Text"] + '\n'
  
  print(fullText)

  table.put_item(Item= {
    'project': user + '/' + project,
    'page': int(page), 
    'text': fullText
    })

  # print(response)
  return 