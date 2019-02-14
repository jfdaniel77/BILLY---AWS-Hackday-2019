import json
import boto3

def lambda_handler(event, context):
    
    client = boto3.client('rekognition')
    
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
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
