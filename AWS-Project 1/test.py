from pprint import pprint
from decimal import Decimal
import boto3
import json
import base64
from boto3.dynamodb.conditions import Key, Attr
import botocore

dynamodb_res = boto3.resource('dynamodb', region_name='us-east-1')
stockid = 'MVY'
price = 100
fiftyTwoWeekHigh = 110
fiftyTwoWeekLow = 80
poi_date = "2021-12-04" #datetime.date.today()
payload_rec = {}
payload_rec['price'] = 100
payload_rec['stockid'] = stockid
payload_rec['fiftyTwoWeekHigh'] = fiftyTwoWeekHigh
payload_rec['fiftyTwoWeekLow'] = fiftyTwoWeekLow
payload_rec['poi_date'] = poi_date
client = boto3.client('sns', region_name='us-east-1')
topic_arn = "arn:aws:sns:us-east-1:318053084668:poi-data-alert"
if price >= (0.8 * fiftyTwoWeekHigh) or price <= (1.2 * fiftyTwoWeekLow):
    print("POI price is", price)
            #payload_rec = json.loads(payload, parse_float=Decimal)
            #poi_date = payload_rec['price_timestamp'].split()[0]
            #payload_rec['poi_date'] = poi_date
    table = dynamodb_res.Table('Stock-poi-data')
    #response = table.query(
     #   KeyConditionExpression=Key('stockid').eq(stockid) & Key('poi_date').eq(poi_date)
    #)
    #resp = table.put_item(Item=payload_rec)
    #if response['Items']:
        #print("data found")
        #payload_rec['price'] = 200
    try:
        resp = table.put_item(
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