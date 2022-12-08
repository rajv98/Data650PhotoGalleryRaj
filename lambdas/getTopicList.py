import json
import base64
import boto3
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):
    # TODO implement
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('photoMetaData')
    
    response = table.scan(AttributesToGet=['topic'])
    
    topics = response["Items"]
    
   # print(topics)
    
    #print(type(topics))
    
    topicList = []
    
    for topic in topics:
        if topic["topic"] not in topicList:
            topicList.append(topic["topic"])
        
    
    print(topicList)
    
    return {
        'topicList': topicList,
        'body': json.dumps('Success')
    }
