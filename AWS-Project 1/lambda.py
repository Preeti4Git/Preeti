from pprint import pprint
import boto3
import json
import base64


def lambda_handler(event, context):
    dynamodb_res = boto3.resource('dynamodb', region_name='us-east-1')

    payload = base64.b64decode(json.dumps(event))
    payload = str(payload, 'utf-8')
    pprint(payload, sort_dicts=False)

    payload_rec = json.loads(payload)
    pprint(payload_rec, sort_dicts=False)
    if payload_rec['price'] >= (0.8 * payload_rec['fiftyTwoWeekHigh']) or payload_rec['price'] <= (1.2 * payload_rec['fiftyTwoWeekLow']):
        print("POI price is", payload_rec['price'])
        poi_date = payload['price_timestamp'].split()[0]
        payload['poi_date'] = poi_date
        table = dynamodb_res.Table('Stock-poi-data')
        response = table.put_item(Item=payload_rec)
        client = boto3.client('sns', region_name='us-east-1')
        topic_arn = "arn:aws:sns:us-east-1:318053084668:poi-data-alert"
        try:
            client.publish(TopicArn=topic_arn, Message="POI detected", Subject = "POI detected")
            result = 1
        except Exception:
            result = 0

    return result