import pandas as pd
from Database import Database

database = Database()

class AggregateModel:
    def calculate_aggregate(self, startTime, endTime):
        #database.createAggTable()
        print(f"Aggregated data from BSM")
        for deviceid in ('HC_101', 'HC_102'):
            for dataType in ('HeartRate','SPO2','Temperature'):
                print(deviceid)
                print(dataType)
                sensordata = database.fetch_time_based_BSM_data(startTime, endTime, dataType, deviceid)
                sensordata['timestamp'] = pd.to_datetime(sensordata['timestamp'])
                timestamps = pd.to_datetime(sensordata['timestamp'])
                sensordata = sensordata.set_index('timestamp')
                min = sensordata.value.resample('min').min()
                max = sensordata.value.resample('min').max()
                mean = pd.to_numeric(sensordata['value']).resample('min').mean()
                for l in min.index:
                   database.insert_BSM_Agg_data(deviceid, dataType, l._repr_base, min[l], max[l], mean[l])

