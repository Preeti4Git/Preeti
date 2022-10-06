import time
from datetime import datetime
from AggregateModel import AggregateModel
from AlertDataModel import AlertDataModel

WAIT_TIME = 0.25

print("\nBSM Simulation started.")
# Creating the edge-server for the communication with the user

aggregate_model = AggregateModel()
alert_data_model = AlertDataModel()

startTime = datetime.strptime('10/31/2021 03:00:00', '%m/%d/%Y %H:%M:%S')
endTime = datetime.strptime('10/31/2021 04:00:00', '%m/%d/%Y %H:%M:%S')

print("\n<<<<<<<<<<<<<<IMPLEMENTATION OF PROBLEM STATEMENT 2 >>>>>>>>>>>>>>")
print("\nDemonstration of BSM data aggregation process.")
aggregate_model.calculate_aggregate(startTime, endTime)

print("\n<<<<<<<<<<<<<<IMPLEMENTATION OF PROBLEM STATEMENT 3 >>>>>>>>>>>>>>")
print("\nDemonstration of checking anomaly data and raising alerts for violations on BSM aggregated data .")
alert_data_model.check_anomalies(startTime, endTime)

print("\nBSM Simulation stopped.")
