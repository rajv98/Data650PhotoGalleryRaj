import json
import base64

import boto3
from boto3.dynamodb.conditions import Attr


s3_uri="s3://data650photogallery/images/" 


def lambda_handler(event, context):
    # TODO implement
    s3_client = boto3.client("s3")
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('photoMetaData')
    
    fileName = event["fileName"]
    
    key = "fullSizeImages/"+fileName;
    
    print(fileName)
    
    s3_client.delete_object(Key=key,
    Bucket = "data650photogallery")
    
    response = table.delete_item(
        Key={
            'photoid': fileName
        }
    )
        
        
    return event
