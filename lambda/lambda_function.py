import json
import boto3

from urllib.parse import urlencode
from urllib.request import Request, urlopen

def lambda_handler(event, context):
    
    client = boto3.client('rekognition')
    
    payload = {}
    
    for record in event['Records']:
        bucketName = record['s3']['bucket']['name']
        objectName = record['s3']['object']['key']
    
        response = client.detect_labels(
            Image={
                'S3Object': {
                    'Bucket': bucketName,
                    'Name': objectName,
                }
            },
            MaxLabels= 123,
            MinConfidence= 80
        )
    
        print('Response = ' + json.dumps(response))
        
        payload["requestID"] = objectName
        payload["data"] = response
    
    #Store into Redis
    url = "https://18.204.42.219:8081/result" # Set destination URL here
    post_fields = payload    # Set POST fields here

    request = Request(url, urlencode(post_fields).encode())
    print(request)
    
    return {
        'statusCode': 200,
        'body': json.dumps(payload)
    }