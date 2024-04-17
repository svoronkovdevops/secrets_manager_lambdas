# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0
import json
import boto3
import time
from calendar import timegm

def handler(event, context):
    
    ddbclient = boto3.client('dynamodb')
    outputstatus = []
    truncate1 = "', {'message_text': {'S': '"
    truncate2 = "[{'message_text': {'S': '"
    truncate3 = "']"
    truncate4 = "'}}, '"

    try:
        messageid = event['Records'][0]['Sns']['MessageId']
        messagetext = event['Records'][0]['Sns']['Message']
        messagets = event['Records'][0]['Sns']['Timestamp']
        utc_time = time.strptime(messagets, "%Y-%m-%dT%H:%M:%S.%fZ")
        epoch_time = str(timegm(utc_time))
        response = ddbclient.put_item(TableName='SNSPortalDDB', Item = {'tablekey': {"S": "1"}, 'message_id': {"S": messageid}, 'message_text': {"S": messagetext}, 'message_ts': {"N": epoch_time}})
    except Exception as e:
        
        putcompliancestatus = ddbclient.scan(TableName='SNSPortalDDB', ProjectionExpression='message_text')
        
        for i in putcompliancestatus['Items']:
            outputstatus.append(i)
            outputstatus.append("<br><br>")

        lst = str(outputstatus)
        f=lst.replace(truncate1,"")
        g=f.replace(truncate2,"")
        h=g.replace(truncate3,"")
        x=h.replace(truncate4,"")

        if(x != "[]"):
            content = "<html><head><meta http-equiv=\"refresh\" content=\"30\"><title>SNS  Portal - AWS Secrets Manager Workshop</title></head><body>%s</body></html>"%(x)
            response = {
                "statusCode": 200,
                "body": content,
                "headers": {
                    'Content-Type': 'text/html' ,
                
                }
            
            }
        else:
            content = "<html><head><meta http-equiv=\"refresh\" content=\"30\"><title>SNS  Portal - AWS Secrets Manager Workshop</title></head><body>No message received yet</body></html>"
            response = {
                "statusCode": 200,
                "body": content,
                "headers": {
                    'Content-Type': 'text/html' ,
                
                }
            
            }
        print(e)
        return response
