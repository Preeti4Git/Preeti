from pprint import pprint
from decimal import Decimal
import boto3
import json
import base64
import botocore

def lambda_handler(event, context):
    dynamodb_res = boto3.resource('dynamodb', region_name='us-east-1')

    for record in event['Records']:
        payload = base64.b64decode(record["kinesis"]["data"])
        payload = str(payload, 'utf-8')
        payload_rec = json.loads(payload)
        pprint(payload_rec, sort_dicts=False)
        if payload_rec['price'] >= (0.8 * payload_rec['fiftyTwoWeekHigh']) or payload_rec['price'] <= (
                1.2 * payload_rec['fiftyTwoWeekLow']):
            print("POI price is", payload_rec['price'])
            payload_rec = json.loads(payload, parse_float=Decimal)
            poi_date = payload_rec['price_timestamp'].split()[0]
            payload_rec['poi_date'] = poi_date
            table = dynamodb_res.Table('Stock-poi-data')
            #response = table.query(
             #   KeyConditionExpression=Key('stockid').eq(payload_rec['stockid']) & Key('poi_date').eq(poi_date)
            #)
            #if response['Items']:
            client = boto3.client('sns', region_name='us-east-1')
            topic_arn = "arn:aws:sns:us-east-1:318053084668:poi-data-alert"
            try:
                response = table.put_item(
                    Item=payload_rec,
                    ConditionExpression='attribute_not_exists(stockid) AND attribute_not_exists(poi_date)'
                )
                client.publish(TopicArn=topic_arn,
                               Message="POI detected for " + payload_rec['stockid'] + " with price being " + str(
                                   payload_rec['price']), Subject="POI detected for " + payload_rec['stockid'])
                result = 1
            except botocore.exceptions.ClientError as e:
                if e.response['Error']['Code'] != 'ConditionalCheckFailedException':
                    raise
            except Exception:
                result = 0