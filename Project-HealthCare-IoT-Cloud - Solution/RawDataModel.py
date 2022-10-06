import boto3
import pandas as pd
from datetime import datetime
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

# Get the service resource.
dynamodb = boto3.resource('dynamodb')

#Query data from table based on device id
def query_BSM_data(deviceid, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('BSM_raw_data')
# Expression attribute names can only reference items in the projection expression.
    response = table.query(
        ProjectionExpression="#deviceid, #timestamp, #datatype, #value",
        ExpressionAttributeNames={"#deviceid": "deviceid","#timestamp": "timestamp","#datatype": "datatype","#value": "value"},
        KeyConditionExpression=
            Key('deviceid').eq(deviceid)
    )
    df = pd.DataFrame(response['Items'])
    return df


# Query data from table based on device id
def fetch_time_based_BSM_data(startTime, endTime, dataType, deviceid, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('BSM_raw_data')

    print(startTime.strftime('%Y-%m-%d %H:%M:%S'))
    print(endTime.strftime('%Y-%m-%d %H:%M:%S'))

    # Expression attribute names can only reference items in the projection expression.
    response = table.query(
        IndexName='datatype-timestamp-index',
        KeyConditionExpression=Key('datatype').eq(dataType) & Key('timestamp').between(startTime.strftime('%Y-%m-%d %H:%M:%S'), endTime.strftime('%Y-%m-%d %H:%M:%S')),
        FilterExpression=Key('deviceid').eq(deviceid)
    )
    df = pd.DataFrame(response['Items'])
    return df


def fetch_all():
    print ('Fetching all data from the DynamoDB table')
    table = dynamodb.Table('BSM_raw_data')
    response = table.scan()
    for item in response['Items']:
        print (item)
    print('Total items in the table are ', response['Count'])


def update_data(deviceid, timestamp, val):
    print ('Update data in DynamoDB table')
    table = dynamodb.Table('BSM_raw_data')
    table.update_item(
        Key={
            'deviceid': deviceid,
            'timestamp': timestamp
        },
        UpdateExpression='SET datatype = :val1',
        ExpressionAttributeValues={
            ':val1': val
        }
    )
    print ('Value updated')


def delete_data(deviceid, timestamp):
    print ('Delete data in DynamoDB table')
    table = dynamodb.Table('BSM_raw_data')
    table.delete_item(
        Key={
            'deviceid': deviceid,
            'timestamp': timestamp
        },
    )
    print ('Item deleted left in the table are ', table.item_count)

