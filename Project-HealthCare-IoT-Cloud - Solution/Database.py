import boto3
import pandas as pd
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

# Get the service resource.
dynamodb = boto3.resource('dynamodb')

class Database:

    def __init__(self):
        # Get the service resource.
        dynamodb = boto3.resource('dynamodb')

    # Create the DynamoDB table.
    '''def createAggTable(self):
        try:
            table = dynamodb.create_table(
            TableName='bsm_agg_data',
            KeySchema=[
                {
                    'AttributeName': 'sensortype',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'timestamp',
                    'KeyType': 'RANGE'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'sensortype',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'timestamp',
                    'AttributeType': 'S'
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )

            # Wait until the table exists.
            table.meta.client.get_waiter('table_exists').wait(TableName='bsm_agg_data')

            # Print out some data about the table.
            print(table.item_count)

        except ClientError as e:
            print ('Exception while table creation' , e.response['Error']['Message'])

    # Create the DynamoDB table.
    def createAlertsTable(self):
        try:
            table = dynamodb.create_table(
                TableName='bsm_alerts',
                KeySchema=[
                    {
                        'AttributeName': 'deviceid#sensortype',
                        'KeyType': 'HASH'
                    },
                    {
                        'AttributeName': 'timestamp',
                        'KeyType': 'RANGE'
                    }
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'deviceid#sensortype',
                        'AttributeType': 'S'
                    },
                    {
                        'AttributeName': 'timestamp',
                        'AttributeType': 'S'
                    },
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                }
            )

            # Wait until the table exists.
            table.meta.client.get_waiter('table_exists').wait(TableName='bsm_alerts')

            # Print out some data about the table.
            print(table.item_count)

        except ClientError as e:
            print('Exception while table creation', e.response['Error']['Message'])
    '''

    # Query data from table based on device id
    def fetch_time_based_BSM_data(self, startTime, endTime, dataType, deviceid, dynamodb=None):
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


    def insert_BSM_Agg_data(self, deviceid, datatype, timestamp, min, max, mean):
        print ('Data Insertion to bsm_agg_data')
        table = dynamodb.Table('bsm_agg_data')
        table.put_item(
           Item={
                'deviceid#sensortype': deviceid+'#'+datatype,
                'deviceid': deviceid,
                'sensortype': datatype,
                'timestamp': timestamp,
                'min': min,
                'max': max,
                'mean': str(mean)
            }
        )

    # Query data from table based on device id
    def fetch_time_based_bsm_agg_data(self, startTime, endTime, dataType, deviceid, dynamodb=None):
        if not dynamodb:
            dynamodb = boto3.resource('dynamodb')

        table = dynamodb.Table('bsm_agg_data')

        print(startTime.strftime('%Y-%m-%d %H:%M:%S'))
        print(endTime.strftime('%Y-%m-%d %H:%M:%S'))

        # Expression attribute names can only reference items in the projection expression.
        response = table.query(
            IndexName='datatype-timestamp-index',
            KeyConditionExpression=Key('deviceid#sensortype').eq(deviceid+"#"+dataType) & Key('timestamp').between(startTime.strftime('%Y-%m-%d %H:%M:%S'), endTime.strftime('%Y-%m-%d %H:%M:%S'))
        )
        #df = pd.DataFrame(response['Items'])
        return response['Items']


    def insert_bsm_alerts_data(self, deviceid, sensorType, timestamp, rule):
        print ('Data Insertion to bsm_alerts')
        table = dynamodb.Table('bsm_alerts')
        table.put_item(
           Item={
                'deviceid#sensortype': deviceid+'#'+sensorType,
                'deviceid': deviceid,
                'sensortype': sensorType,
                'timestamp': timestamp,
                'rule': rule
            }
        )