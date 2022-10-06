import boto3
import pandas as pd
from datetime import datetime
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

# Get the service resource.
dynamodb = boto3.resource('dynamodb')

# Create the DynamoDB table.
def createTable():
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
    '''response = table.query(
        ProjectionExpression="#deviceid, #timestamp, #datatype, #value",
        ExpressionAttributeNames={"#deviceid": "deviceid", "#timestamp": "timestamp", "#datatype": "datatype",
                                  "#value": "value"},
        KeyConditionExpression=
        Key('datatype').eq(dataType) & Key('timestamp').between(startTime.strftime('%Y-%m-%d'), endTime.strftime('%Y-%m-%d'))
    )'''
    response = table.query(
        IndexName='datatype-timestamp-index',
        KeyConditionExpression=Key('datatype').eq(dataType) & Key('timestamp').between(startTime.strftime('%Y-%m-%d %H:%M:%S'), endTime.strftime('%Y-%m-%d %H:%M:%S')),
        FilterExpression=Key('deviceid').eq(deviceid)
    # Key('deviceid').eq(deviceid) & Key('timestamp').begins_with(start_date.strftime('%m/%d/%Y'))
    )
    df = pd.DataFrame(response['Items'])
    return df
    # return df.set_index('timestamp').resample('H').sum().reset_index()

def insert_BSM_data(datatype, timestamp, deviceid, value):
    print ('Data Insertion')
    table = dynamodb.Table('BSM_raw_data')
    table.put_item(
       Item={
            'datatype': datatype,
            'timestamp': timestamp,
            'deviceid': deviceid,
            'value': value
        }
    )
    print ('Total items in the table are ', table.item_count)

def insert_BSM_Agg_data(deviceid, datatype, timestamp, min, max, mean):
    print ('Data Insertion to bsm_agg_data')
    table = dynamodb.Table('bsm_agg_data')
    table.put_item(
       Item={
            'deviceid#sensortype': deviceid+'#'+dataType,
            'deviceid': deviceid,
            'sensortype': datatype,
            'timestamp': timestamp,
            'min': min,
            'max': max,
            'mean': str(mean)
        }
    )
    print ('Total items in the table are ', table.item_count)

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

if __name__ == '__main__':
    createTable()
    print(f"Aggregated data from BSM")
    startTime = datetime.strptime('10/29/2021 18:37:00', '%m/%d/%Y %H:%M:%S')
    endTime = datetime.strptime('10/29/2021 19:37:00', '%m/%d/%Y %H:%M:%S')
    for deviceid in ('HC_101', 'HC_102'):
        for dataType in ('HeartRate','SPO2','Temperature'):
            print(deviceid)
            sensordata = fetch_time_based_BSM_data(startTime, endTime, dataType, deviceid)
            sensordata['timestamp'] = pd.to_datetime(sensordata['timestamp'])
            timestamps = pd.to_datetime(sensordata['timestamp'])
            sensordata = sensordata.set_index('timestamp')
            min = sensordata.value.resample('min').min()
            max = sensordata.value.resample('min').max()
            mean = pd.to_numeric(sensordata['value']).resample('min').mean()
            print(dataType)
            print('min', min)
            print('max', max)
            print('mean', mean)
            print(min.index)
            print(min[min.index])
            for l in min.index:
               insert_BSM_Agg_data(deviceid, dataType, l._repr_base, min[l], max[l], mean[l])

    #sensordata['ts'] = pd.to_datetime((sensordata['timestamp']))
    #sensordata[sensordata.ts.dt.strftime('%H:%M:%S').between('00:00:00', '12:00:00')]
    #print (sensordata)
    #times = pd.to_datetime(df.timestamp_col)
    #df.groupby([times.hour, times.minute]).value_col.sum()