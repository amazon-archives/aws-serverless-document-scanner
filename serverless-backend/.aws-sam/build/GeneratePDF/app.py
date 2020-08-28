import os
import json, decimal
import boto3
import base64
from fpdf import FPDF 
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

  def decimal_default(obj):
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    raise TypeError

  pdf = FPDF() 
  
  pdf.set_font("Arial", size = 11) 
  
  for item in data:
    pdf.add_page() 
    pdf.multi_cell(0, 8, item['text'], 0, 0, '')
    
  output = pdf.output(dest='S').encode('latin-1')
  output = "data:application/pdf;base64," + base64.b64encode(output).decode('utf-8')
  
  body = {
    "url": output
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