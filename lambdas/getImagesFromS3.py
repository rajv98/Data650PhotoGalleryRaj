import json

import boto3
from boto3.dynamodb.conditions import Attr

s3_uri="s3://data650photogallery/fullSizeImages/" 


def list_s3_files_using_client(bucket,prefix,s3_client,topic):

    response = s3_client.list_objects_v2(Bucket=bucket,  Prefix=prefix) 
    files = response.get("Contents")
    files.reverse()
    
  
    urls = []

    for file in files: 
        file_path=file['Key']
        #print(file_path)
        if file_path.endswith(".jpg") or file_path.endswith(".png"):
            if topic in file_path:
                object_url="https://"+bucket+".s3.amazonaws.com/"+file_path 
                urls.append(object_url)
           # print(object_url)
        
    return urls


def lambda_handler(event, context):
    # TODO implement
    arr=s3_uri.split('/')
    bucket =arr[2]
    prefix=""
    
    for i in range(3,len(arr)-1):
        prefix=prefix+arr[i]+"/"
        
    s3_client = boto3.client("s3")
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('photoMetaData')
    
    topic = event["topic"]

    url_list = list_s3_files_using_client(bucket=bucket,prefix=prefix,s3_client=s3_client,topic=topic)
    
    if topic != "":
        response = table.scan(FilterExpression=Attr('topic').eq(topic))
    else:
        response = table.scan()

        
   # print(response["Items"])

    details = response["Items"]
    
    details = sorted(details, key=lambda d: d['timestamp'], reverse=True) 
    
    for detail in details:
        
        photoId = detail["photoid"]
        object_url="https://"+bucket+".s3.amazonaws.com/"+"fullSizeImages/"+photoId
        
        detail["photoid"]=object_url
       # print(object_url)
        
    
    
    #print(url_list)
    
    event['url_list']=  url_list
    event['details']= details
    
    return event
