import json
import base64
import datetime


import boto3
from time import gmtime, strftime

# create a DynamoDB object using the AWS SDK

s3_uri="s3://data650photogallery/images/" # S3 URI of the folder you want to recursively scan, Replace this with your own S3 URI

def lambda_handler(event, context):
    
    s3_client = boto3.client("s3")
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('photoMetaData')

    
    imgBase = event["imageBase64"]
    
    fileType =  imgBase.split(",")[0];
    imgBase = imgBase.split(",")[1];

    print(fileType)

    caption = event["caption"]
    captionFileName = caption.replace(" ","_")
    
    print(caption)
    
    decoded_image = base64.b64decode(imgBase)
    

    
    # get current time
    now= datetime.datetime.now()
    
    now = now + datetime.timedelta(hours=-5)
    
    nowDb = now.strftime("%d %b %Y %H:%M:%S")
    
    nowFileName = now.strftime("%d%b%Y%H_%M_%S")
    
    print(nowDb)
    print(nowFileName)
    
    username = event['username']
    
    key = "fullSizeImages/"+nowFileName+"_"+captionFileName+"_"+username
    keyDb = nowFileName+"_"+captionFileName+"_"+username
    
     
    if "jpg" in fileType or "jpeg" in fileType:
    
        key = key+".jpg";
        keyDb = keyDb+".jpg";
        
        s3_client.put_object(Key=key,
        Body=decoded_image,
        ContentType="image/jpeg",
        Bucket = "data650photogallery")
        
        event["ThisFromLambDa"]="JustSoYaKnowJpEG"
         
    if "png" in fileType: 
        
        key = key+".png";
        keyDb = keyDb+".png";
        
        s3_client.put_object(Key=key,
        Body=decoded_image,
        ContentType="image/png",
        Bucket = "data650photogallery")
        
        event["ThisFromLambDa"]="JustSoYaKnowPNG"
         
    table.put_item(
            Item={
            'photoid': keyDb,
            'username':username,
            'topic':caption,
            'timestamp':nowDb
            })   
    
    
    return event