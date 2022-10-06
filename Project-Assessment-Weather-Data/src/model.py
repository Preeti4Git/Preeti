# Imports Database class from the project to provide basic functionality for database access
from database import Database
# Imports ObjectId to convert to the correct format before querying in the db
from bson.objectid import ObjectId


# User document contains username (String), email (String), and role (String) fields
class UserModel:
    USER_COLLECTION = 'users'

    def __init__(self):
        self._db = Database()
        self._latest_error = ''

    # Latest error is used to store the error string in case an issue. Is reset at the beginning of a new function call
    @property
    def latest_error(self):
        return self._latest_error

    # Since username should be unique in users collection,
    # this provides a way to fetch the user document based on the username
    def find_by_username(self, username):
        key = {'username': username}
        return self.__find(key)
    
    # Finds a document based on the unique auto-generated MongoDB object id 
    def find_by_object_id(self, obj_id):
        key = {'_id': ObjectId(obj_id)}
        return self.__find(key)
    
    # Private function (starting with __) to be used as the base for all find functions
    def __find(self, key):
        user_document = self._db.get_single_data(UserModel.USER_COLLECTION, key)
        return user_document
    
    # This first checks if a user already exists with that username.
    # If it does, it populates latest_error and returns -1
    # If a user doesn't already exist, it'll insert a new document and return the same to the caller
    def insert(self, username, email, role):
        self._latest_error = ''
        user_document = self.find_by_username(username)
        if user_document:
            self._latest_error = f'Username {username} already exists'
            return -1
        
        user_data = {'username': username, 'email': email, 'role': role}
        user_obj_id = self._db.insert_single_data(UserModel.USER_COLLECTION, user_data)
        return self.find_by_object_id(user_obj_id)

    # This first checks if the user to be deleted exists. If it does, it deletes that entry.
    # If it doesn't exist, it populates latest_error and returns -1.
    def delete(self, username):
        self._latest_error = ''
        user_document = self.find_by_username(username)
        if user_document == -1:
            self._latest_error = f'Data for user {username} does not exist, so nothing to delete'
            return -1
        else:
            key = {'username': username}
            deleteAck = self._db.delete_single_data(UserModel.USER_COLLECTION, key)
            return deleteAck

    # This first checks if the user exists to be updated. If it does not, it populates latest_error and returns -1
    # If a user does exist, it'll update the document and return the same to the caller
    def update(self, username, param, value):
        self._latest_error = ''
        user_document = self.find_by_username(username)
        if user_document is None:
            self._latest_error = f'Username {username} does not exist'
            return -1

        filter_value = {'username':username}
        update_value = {"$set":{param : value}}
        update_ack = self._db.update_single_data(UserModel.USER_COLLECTION, filter_value, update_value)
        return update_ack

# Device document contains device_id (String), desc (String),
# type (String - temperature/humidity) and manufacturer (String) fields


class DeviceModel:
    DEVICE_COLLECTION = 'devices'

    def __init__(self):
        self._db = Database()
        self._latest_error = ''
    
    # Latest error is used to store the error string in case an issue. Is reset at the beginning of a new function call
    @property
    def latest_error(self):
        return self._latest_error
    
    # Since device id should be unique in devices collection,
    # this provides a way to fetch the device document based on the device id
    def find_by_device_id(self, device_id):
        key = {'device_id': device_id}
        return self.__find(key)
    
    # Finds a document based on the unique auto-generated MongoDB object id 
    def find_by_object_id(self, obj_id):
        key = {'_id': ObjectId(obj_id)}
        return self.__find(key)
    
    # Private function (starting with __) to be used as the base for all find functions
    def __find(self, key):
        device_document = self._db.get_single_data(DeviceModel.DEVICE_COLLECTION, key)
        return device_document
    
    # This first checks if a device already exists with that device id.
    # If it does, it populates latest_error and returns -1
    # If a device doesn't already exist, it'll insert a new document and return the same to the caller
    def insert(self, device_id, desc, type, manufacturer):
        self._latest_error = ''
        device_document = self.find_by_device_id(device_id)
        if device_document:
            self._latest_error = f'Device id {device_id} already exists'
            return -1
        
        device_data = {'device_id': device_id, 'desc': desc, 'type': type, 'manufacturer': manufacturer}
        device_obj_id = self._db.insert_single_data(DeviceModel.DEVICE_COLLECTION, device_data)
        return self.find_by_object_id(device_obj_id)

    # This first checks if a device exists with that device id. If it does not, it populates latest_error and returns -1
    # If a device does exist, it'll update the document and return the same to the caller
    def update(self, device_id, param, value):
        self._latest_error = ''
        device_document = self.find_by_device_id(device_id)
        if device_document is None:
            self._latest_error = f'Device id {device_id} does not exist'
            return -1

        filter_value = {'device_id':device_id}
        update_value = {"$set":{param : value}}
        update_ack = self._db.update_single_data(DeviceModel.DEVICE_COLLECTION, filter_value, update_value)
        return update_ack

    # This first checks if a device exists with that device id. If it does not, it populates latest_error and returns -1
    # If a device does exist, it'll update the document and return the same to the caller
    def delete(self, device_id):
        self._latest_error = ''
        device_document = self.find_by_device_id(device_id)
        if device_document is None:
            self._latest_error = f'Device id {device_id} does not exist'
            return -1

        filter_value = {'device_id': device_id}
        delete_ack = self._db.delete_single_data(DeviceModel.DEVICE_COLLECTION, filter_value)
        return delete_ack


# Weather data document contains device_id (String), value (Integer), and timestamp (Date) fields
class WeatherDataModel:
    WEATHER_DATA_COLLECTION = 'weather_data'

    def __init__(self):
        self._db = Database()
        self._latest_error = ''
    
    # Latest error is used to store the error string in case an issue. It's reset at the beginning of a new function call
    @property
    def latest_error(self):
        return self._latest_error
    
    # Since device id and timestamp should be unique in weather_data collection, this provides a way to fetch the data document based on the device id and timestamp
    def find_by_device_id_and_timestamp(self, device_id, timestamp):
        key = {'device_id': device_id, 'timestamp': timestamp}
        return self.__find(key)
    
    # Finds a document based on the unique auto-generated MongoDB object id 
    def find_by_object_id(self, obj_id):
        key = {'_id': ObjectId(obj_id)}
        return self.__find(key)
    
    # Private function (starting with __) to be used as the base for all find functions
    def __find(self, key):
        wdata_document = self._db.get_single_data(WeatherDataModel.WEATHER_DATA_COLLECTION, key)
        return wdata_document
    
    # This first checks if a data item already exists at a particular timestamp for a device id.
    # If it does, it populates latest_error and returns -1.
    # If it doesn't already exist, it'll insert a new document and return the same to the caller
    def insert(self, device_id, value, timestamp):
        self._latest_error = ''
        wdata_document = self.find_by_device_id_and_timestamp(device_id, timestamp)
        if wdata_document:
            self._latest_error = f'Data for timestamp {timestamp} for device id {device_id} already exists'
            return -1
        
        weather_data = {'device_id': device_id, 'value': value, 'timestamp': timestamp}
        wdata_obj_id = self._db.insert_single_data(WeatherDataModel.WEATHER_DATA_COLLECTION, weather_data)
        return self.find_by_object_id(wdata_obj_id)

    # This first checks if a data item exists at a particular timestamp for a device id.
    # If it does, it deletes that entry.
    # If it doesn't exist, it populates latest_error and returns -1.
    def delete(self, device_id, timestamp):
        self._latest_error = ''
        wdata_document = self.find_by_device_id_and_timestamp(device_id, timestamp)
        if wdata_document == -1:
            self._latest_error = f'Data for timestamp {timestamp} for device id {device_id} does not exist, so nothing to delete'
            return -1
        else:
            key = {'device_id': device_id, 'timestamp': timestamp}
            delete_ack = self._db.delete_single_data(WeatherDataModel.WEATHER_DATA_COLLECTION, key)
            return delete_ack

    # This first checks if the device data exists to be updated.
    # If it does not, it populates latest_error and returns -1
    # If the data does exist, it'll update the document and return the same to the caller
    def update(self, device_id, timestamp, param, value):
        self._latest_error = ''
        weather_data = self.find_by_device_id_and_timestamp(device_id, timestamp)
        if weather_data is None:
            self._latest_error = f'Data does not exist to be updated'
            return -1

        filter_value = {'device_id':device_id, 'timestamp':timestamp}
        update_value = {"$set":{param : value}}
        update_ack = self._db.update_single_data(WeatherDataModel.WEATHER_DATA_COLLECTION, filter_value, update_value)
        return update_ack


# User Device document contains username (String), access_type (Array) fields


class UserDeviceModel:
    USER_DEVICE_COLLECTION = 'user_device_access'

    def __init__(self):
        self._db = Database()
        self._latest_error = ''

    # Latest error is used to store the error string in case an issue. Is reset at the beginning of a new function call
    @property
    def latest_error(self):
        return self._latest_error

    # Since user id should be unique in user_device_access collection,
    # this provides a way to fetch the user device access document based on the user id
    def find_access_by_username(self, username):
        key = {'username': username}
        return self.__find(key)

    # Finds a document based on the unique auto-generated MongoDB object id
    def find_by_object_id(self, obj_id):
        key = {'_id': ObjectId(obj_id)}
        return self.__find(key)

    # Private function (starting with __) to be used as the base for all find functions
    def __find(self, key):
        user_device_document = self._db.get_single_data(UserDeviceModel.USER_DEVICE_COLLECTION, key)
        return user_device_document

# User Device document contains username (String), access_type (Array) fields
class DailyReportModel:
    DAILY_REPORTS_COLLECTION = 'daily_reports'

    def __init__(self):
        self._db = Database()
        self._latest_error = ''

    # Latest error is used to store the error string in case an issue. Is reset at the beginning of a new function call
    @property
    def latest_error(self):
        return self._latest_error

    # Report aggregate data functionality included to directly aggregate reports from weather data
    # and store in daily_reports collection
    def aggregate(self):
        self._latest_error = ''
        try:
            group_pipeline = {"$group": {"_id": {"device_id": "$device_id", "date" : { "$dateToString" : { "format": "%Y-%m-%d", "date": "$timestamp" }}}, "average" : { "$avg" : "$value"}, "minimum" : { "$min" : "$value"}, "maximum" : { "$max" : "$value"}}}
            out_pipeline = { "$out": DailyReportModel.DAILY_REPORTS_COLLECTION}
            pipeline = [group_pipeline, out_pipeline]
            data_document = self._db.aggregate_data(WeatherDataModel.WEATHER_DATA_COLLECTION, pipeline)
            return data_document
        except :
            self._latest_error = 'Error while aggregating and inserting weather data into daily_reports'
            return -1

    # Fetching count of rows in report data functionality included to verify the count of rows in daily_reports.
    def count_report_data(self):
        self._latest_error = ''
        try:
            pipeline = [{"$count" : "rows"}]
            report_data = self._db.aggregate_data(DailyReportModel.DAILY_REPORTS_COLLECTION, pipeline)
            for result in report_data:
                rows = result["rows"]
            return rows
        except Exception:
            self._latest_error = 'Error while counting rows in daily_reports'
            return -1

    # Fetching report data functionality included using match aggregation function
    def fetch_report(self, device_id, start_date, end_date):
        self._latest_error = ''
        try:
            pipeline = [{"$match":{"_id.device_id": device_id, "_id.date": {"$lte": end_date, "$gte": start_date }}}]
            report_data = self._db.aggregate_data(DailyReportModel.DAILY_REPORTS_COLLECTION, pipeline)
            return report_data
        except Exception:
            self._latest_error = 'Error while fetching reports data from daily_reports'
            return -1
