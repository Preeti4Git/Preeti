from authservice import UserModelService, DeviceModelService, WeatherDataModelService, UserDeviceModelService, \
    DailyReportModelService
from datetime import datetime

# Assumption that login username can be fetched from session, hardcoding the username below for demonstration purpose
login_username_default = 'user_1'
login_username_admin = 'admin'

# Demonstration of CRUD operations in the users collection based on login username and its role
user_coll_default = UserModelService(login_username_default)
user_coll_admin = UserModelService(login_username_admin)

login_user_role_default = user_coll_default.login_user_role
login_user_role_admin = user_coll_admin.login_user_role

user_device_coll = UserDeviceModelService()
access_list_default = user_device_coll.find_access_by_username(login_username_default)
access_list_admin = user_device_coll.find_access_by_username(login_username_admin)

print('\n\n---------User data operations demonstrated below-------------')

# Shows failed attempt to read user data with default user
print(f'\nTrying to read user data with default user, so should fail -->')
user_document = user_coll_default.find_by_username('user_2')
if user_document == -1:
    print(user_coll_default.latest_error)
else:
    print(f'User data read --> {user_document}')

# Shows successful attempt to read user data with admin user
print(f'\nDemonstrate read user data with admin user, so should succeed -->')
user_document = user_coll_admin.find_by_username('user_2')
if user_document == -1:
    print(user_coll_admin.latest_error)
else:
    print(f'User data read --> {user_document}')

# Shows a failed attempt to insert user data with default user user_1
print(f'\nDemonstrate insert user data with default user user_1, so should fail -->')
user_document = user_coll_default.insert('test_3', 'test_3@example.com', 'default')
if user_document == -1:
    print(user_coll_default.latest_error)
else:
    print(f'User data inserted --> {user_document}')

# Shows a successful attempt on how to insert a user
print(f'\nDemonstrate delete and insert user data (so that no constraint violation is raised) with '
      f'admin user, so should succeed. Delete not needed in production code, instead can throw relevant message -->')
user_document_del = user_coll_admin.delete('test_3')
user_document = user_coll_admin.insert('test_3', 'test_3@example.com', 'default')
if user_document == -1:
    print(user_coll_admin.latest_error)
else:
    print(f'User data inserted --> {user_document}')

# Shows a failed attempt to update user data with default user user_1
print(f'\nDemonstrate update user data with default user user_1, so should fail -->')
updateAck = user_coll_default.update('test_3', 'email', 'test_3_changed@example.com')
if updateAck == -1:
    print(user_coll_default.latest_error)
else:
    print(f'User data updated successfully')
    user_document = user_coll_admin.find_by_username('test_3')
    print(f'Updated data --> {user_document}')

# Shows a successful attempt to update user data with admin user
print(f'\nDemonstrate update user data with admin user, so should succeed -->')
updateAck = user_coll_admin.update('test_3', 'email', 'test_3_changed@example.com')
if updateAck == -1:
    print(user_coll_admin.latest_error)
else:
    print(f'User data updated successfully')
    user_document = user_coll_admin.find_by_username('test_3')
    print(f'Updated data --> {user_document}')

# Shows how to initiate and search in the devices collection based on a device id
device_coll_default = DeviceModelService(login_user_role_default, access_list_default)
device_coll_admin = DeviceModelService(login_user_role_admin, access_list_admin)

print('\n\n---------Device data operations demonstrated below-------------')
# Find device data where default user has read/write access
print(f'\nTrying to read device data for device DT002 where default user has read/write access, so should succeed -->')
device_document = device_coll_default.find_by_device_id('DT002')
if device_document == -1:
    print(device_coll_default.latest_error)
else:
    print(f'Device read successfully {device_document}')

# Find device data where default user does not have read access
print(f'\nTrying to read device data for device DT004 where default user does not have read access, so should fail -->')
device_document = device_coll_default.find_by_device_id('DT004')
if device_document == -1:
    print(device_coll_default.latest_error)
else:
    print(f'Device read successfully {device_document}')

# Find device data where admin user
print(f'\nTrying to read device data for device DT004 by admin user, so should succeed -->')
device_document = device_coll_admin.find_by_device_id('DT004')
if device_document == -1:
    print(device_coll_admin.latest_error)
else:
    print(f'Device read successfully {device_document}')

# Shows a attempt on how to insert a new device
print(f"\nTrying to insert device data for device DT201 where default user user_1 "
      f"does not have any access specified since it is a new device, so should fail -->")
device_document = device_coll_default.insert('DT201', 'Temperature Sensor', 'Temperature', 'Acme')
if device_document == -1:
    print(device_coll_default.latest_error)
else:
    print(f'Device inserted successfully {device_document}')

# Shows a successful attempt on how to insert a new device with admin user
# Deleting the data before inserting in this scenario, to demonstrate insertion without constraint violation
print(f'\nTrying to insert device data for device DT301 with admin user, so should succeed -->')
device_document = device_coll_admin.delete('DT301')
device_document = device_coll_admin.insert('DT301', 'Temperature Sensor', 'Temperature', 'Acme')
if device_document == -1:
    print(device_coll_admin.latest_error)
else:
    print(f'Device inserted successfully {device_document}')

# Shows a successful attempt on how to update a device if user has write access to the device
print(
    f'\nTrying to update device data for device DT002 where default user user_1 has write access, so should succeed -->')
updateAck = device_coll_default.update('DT002', 'manufacturer', 'Ace')
if updateAck == -1:
    print(device_coll_default.latest_error)
else:
    print(f'Device updated successfully')
    device_document = device_coll_admin.find_by_device_id('DT002')
    print(f'Updated data --> {device_document}')

# Shows a failed attempt on how to update a device in absence of write access
print(f'\nTrying to update device data for device DT001 where default user user_1 '
      f'has read access only, so should fail -->')
updateAck = device_coll_default.update('DT001', 'manufacturer', 'Ace')
if updateAck == -1:
    print(device_coll_default.latest_error)
else:
    print(f'Device updated successfully')
    device_document = device_coll_admin.find_by_device_id('DT001')
    print(f'Updated data --> {device_document}')

# Shows a successful attempt to update a device with admin user
print(f'\nTrying to update device data for device DT002 with admin user, so should succeed -->')
updateAck = device_coll_admin.update('DT002', 'manufacturer', 'Acme')
if updateAck == -1:
    print(device_coll_admin.latest_error)
else:
    print(f'Device updated successfully')
    device_document = device_coll_admin.find_by_device_id('DT002')
    print(f'Updated data --> {device_document}')

# Create weather data handling service objects for admina nd non-admin users to demonstrate the specific behaviours
wdata_coll_default = WeatherDataModelService(login_user_role_default, access_list_default)
wdata_coll_admin = WeatherDataModelService(login_user_role_admin, access_list_admin)

print('\n\n---------Weather data operations demonstrated below-------------')

# Shows how to initiate and search in the weather_data collection based on a device_id and timestamp
# Successful weather data read by user having read access on device
print(f'\nTrying to read/fetch weather data for device DT001 where default user user_1 has read access, '
      f'so should succeed -->')
wdata_document = wdata_coll_default.find_by_device_id_and_timestamp('DT001', datetime(2020, 12, 2, 13, 30, 0))
if wdata_document == -1:
    print(wdata_coll_default.latest_error)
else:
    print(f'Weather data for device successfully read by user {login_username_default} as {wdata_document}')

# Initiate and search in the weather_data collection based on a device_id and timestamp
# Failed weather data read by user having no read access on device
print(f'\nTrying to read/fetch weather data for device DT003 where '
      f'default user user_1 does not have read access, so should fail -->')
wdata_document = wdata_coll_default.find_by_device_id_and_timestamp('DT003', datetime(2020, 12, 2, 13, 30, 0))
if wdata_document == -1:
    print(wdata_coll_default.latest_error)
else:
    print(f'Weather data for device successfully read by user {login_username_default} as {wdata_document}')

# Initiate and search in the weather_data collection based on a device_id and timestamp
# Successful weather data read by admin user
print(f'\nTrying to read/fetch weather data for device DT004 with admin user, so should succeed -->')
wdata_document = wdata_coll_admin.find_by_device_id_and_timestamp('DT004', datetime(2020, 12, 2, 13, 30, 0))
if wdata_document == -1:
    print(wdata_coll_admin.latest_error)
else:
    print(f'Weather data for device successfully read by user {login_username_admin} as {wdata_document}')

# Shows a failed attempt on how to insert a new data point
print(f'\nTrying to insert weather data for device DT002 where default user user_1 has read and write access '
      f'but data already exists so there is constraint violation -->')
wdata_document = wdata_coll_default.insert('DT002', 12, datetime(2020, 12, 2, 13, 30, 0))
if wdata_document == -1:
    print(wdata_coll_default.latest_error)
else:
    print(f'Successfully deleted and inserted following weather data as user has write access '
          f'on the device : {wdata_document}')

# Shows a successful attempt on how to delete and insert a new data point with user having write access on the device
# First deleting the data if already exists so that there is no constraint violation.
print(f'\nDeleting and Inserting weather data for device DT002 where default user user_1 has read and write access -->')
wdata_coll_default.delete('DT002', datetime(2020, 12, 7, 13, 30, 0))
wdata_document = wdata_coll_default.insert('DT002', 12, datetime(2020, 12, 7, 13, 30, 0))
if wdata_document == -1:
    print(wdata_coll_default.latest_error)
else:
    print(f'Successfully deleted and inserted following weather data as user has write access on the '
          f'device : {wdata_document}')

# Shows a failed attempt on inserting a new data point with user having no write access on the device
print(f'\nInserting weather data for device DT001 where default user user_1 has only read access, so should fail -->')
wdata_document = wdata_coll_default.delete('DT001', datetime(2020, 12, 7, 13, 30, 0))
wdata_document = wdata_coll_default.insert('DT001', 12, datetime(2020, 12, 7, 13, 30, 0))
if wdata_document == -1:
    print(wdata_coll_default.latest_error)
else:
    print(f'Successfully deleted and inserted following weather data as user has write access on the '
          f'device : {wdata_document}')

# Shows a successful attempt on inserting a new data point with admin user
print(f'\nInserting weather data for device DT001 with admin user -->')
wdata_coll_admin.delete('DT001', datetime(2020, 12, 8, 13, 30, 0))
wdata_document = wdata_coll_admin.insert('DT001', 12, datetime(2020, 12, 8, 13, 30, 0))
if wdata_document == -1:
    print(wdata_coll_admin.latest_error)
else:
    print(f'Successfully deleted and inserted following weather data as user has write access on the '
          f'device : {wdata_document}')

# Shows a successful attempt on updating a data point with default user user_1 for device with write access
print(f'\nUpdating weather data for device DT002 with default user for device with write access-->')
updateAck = wdata_coll_default.update('DT002', datetime(2020, 12, 5, 13, 30, 0), 'value', 11)
if updateAck == -1:
    print(wdata_coll_default.latest_error)
else:
    print(f'Successfully updated weather data as user has write access on the device')
    wdata_document = wdata_coll_default.find_by_device_id_and_timestamp('DT002', datetime(2020, 12, 5, 13, 30, 0))
    print(f'Updated data --> {wdata_document}')

# Shows a failed attempt on updating a data point with default user user_1 for device without write access
print(f'\nUpdating weather data for device DT001 with default user for device without write access-->')
updateAck = wdata_coll_default.update('DT001', datetime(2020, 12, 5, 13, 30, 0), 'value', 12)
if updateAck == -1:
    print(wdata_coll_default.latest_error)
else:
    print(f'Successfully updated weather data as user has write access on the device')
    wdata_document = wdata_coll_default.find_by_device_id_and_timestamp('DT001', datetime(2020, 12, 5, 13, 30, 0))
    print(f'Updated data --> {wdata_document}')

# Shows a successful attempt on updating a data point with admin user
print(f'\nUpdating weather data for device DT001 with admin user -->')
updateAck = wdata_coll_admin.update('DT001', datetime(2020, 12, 5, 13, 30, 0), 'value', 10)
if updateAck == -1:
    print(wdata_coll_admin.latest_error)
else:
    print(f'Successfully updated weather data as user has write access on the device')
    wdata_document = wdata_coll_admin.find_by_device_id_and_timestamp('DT001', datetime(2020, 12, 5, 13, 30, 0))
    print(f'Updated data --> {wdata_document}')

# Changes for fetching daily reports data
report_coll_default = DailyReportModelService(login_user_role_default)
report_coll_admin = DailyReportModelService(login_user_role_admin)

print('\n\n---------Daily reports data operations demonstrated below-------------')

# 2(b) Failed Aggregate daily weather data into daily_reports collection,
# according to device ID and date, by default user user_1
print('\n2(b). Insert aggregated daily weather data into daily_reports collection, according to device ID '
      'and date, by default user user_1')
aggregatedData = report_coll_default.aggregate()
if aggregatedData == -1:
    print(report_coll_default.latest_error)
else:
    print('Data successfully inserted into daily reports collection')

# 2(b) Successful Aggregate daily weather data into daily_reports collection,
# according to device ID and date by admin user
print('\n2(b). Insert aggregated daily weather data into daily_reports collection, '
      'according to device ID and date by admin user')
aggregatedData = report_coll_admin.aggregate()
if aggregatedData == -1:
    print(report_coll_admin.latest_error)
else:
    print('Data successfully inserted into daily reports collection')

# Verify the count of rows in daily_reports collection by admin user
print('\n Verify the count of rows in daily_reports collection inserted with data aggregator function')
aggregatedData = report_coll_admin.count_report_data()
if aggregatedData == -1:
    print(report_coll_admin.latest_error)
else:
    print(f'Daily_reports has {aggregatedData} rows (50 inserted from setup.py and 2 inserted '
          f'as part of access demonstration into weather_data collection above)')

# 2(c) Demonstrate failed fetching aggregated weather data with input as device ID along with start date
# and end date, using default user
print('\n2(c). Demonstrate failed fetching aggregated weather data with input as device ID alongwith '
      'start date and end date, using default user -->')
reportData = report_coll_default.fetch_report('DT001', '2020-12-01', '2020-12-02')
if reportData == -1:
    print(report_coll_default.latest_error)
else:
    for result in reportData:
        print(result)

# 2(c) Demonstrate successful fetching aggregated weather data with input as device ID
# along with start date and end date, using admin
print('\n2(c). Demonstrate successful fetching aggregated weather data with input as device ID '
      'alongwith start date and end date, using admin -->')
reportData = report_coll_admin.fetch_report('DT001', '2020-12-01', '2020-12-02')
if reportData == -1:
    print(report_coll_admin.latest_error)
else:
    for result in reportData:
        print(result)
