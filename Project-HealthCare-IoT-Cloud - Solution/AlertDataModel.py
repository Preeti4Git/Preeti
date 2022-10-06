import boto3
import json
from datetime import datetime
from Database import Database

# Get the service resource.
dynamodb = boto3.resource('dynamodb')

database = Database()

class AlertDataModel:
    def check_anomalies(self, startTime, endTime):
        #database.createAlertsTable()
        print(f'Checking for anomalies on BSM aggregarted data')
        # Reading the rules file
        f = open("rules.json")
        rules = json.loads(f.read())
        f.close()
        # Initializing connection to the database
        for rule in rules:
            count=0
            rule_name = rules[rule]["rule_name"]
            sensortype = rules[rule]["type"]
            avg_min = rules[rule]["avg_min"]
            avg_max = rules[rule]["avg_max"]
            trigger_count = rules[rule]["trigger_count"]
            for deviceid in ('HC_101', 'HC_102'):
                print(deviceid)
                sensordata = database.fetch_time_based_bsm_agg_data(startTime, endTime, sensortype, deviceid)
                for data in sensordata:
                    if (float(data['mean']) < avg_min) or (float(data['mean']) > avg_max):
                        print(f'Anomaly detected {count}')
                        if count == 0:
                            time_breach = data['timestamp']
                        count += 1
                        if count >= trigger_count:
                            print(f'BSM alert raised for rule : {rule_name} on device : {deviceid} for the sensor : {sensortype} at time : {time_breach}')
                            database.insert_bsm_alerts_data(deviceid, sensortype, time_breach, rule_name)
                            count = 0
                            time_breach = 0
                    else:
                        count = 0
                        time_breach = 0

