from model import UserModel, DeviceModel, WeatherDataModel, UserDeviceModel, DailyReportModel

# User document contains username (String), email (String), and role (String) fields


class UserModelService:
    def __init__(self, login_username):
        self._userModel = UserModel()
        self._latest_error = ''
        self._login_user_name = login_username
        self._login_user_role = self.find_login_user_role(self._login_user_name)

    # Latest error is used to store the error string in case an issue. Is reset at the beginning of a new function call
    @property
    def latest_error(self):
        return self._latest_error

    @property
    def login_user_role(self):
        return self._login_user_role

    # fetch the role of logged in user whether admin or default, so sufficient privileges can be provided.
    # Assigned during object creation.
    def find_login_user_role(self, login_username):
        self._latest_error = ''
        try:
            user = self._userModel.find_by_username(login_username)
            if (user is None):
                return 'default'
            else:
                return user['role']
        except:
            self._latest_error = f'Error while trying to fetch logged in user\'s role'
            return -1

    # Since username should be unique in users collection,
    # this provides a way to fetch the user document based on the username
    # Only admin users have access to read data
    def find_by_username(self, username):
        self._latest_error = ''
        try:
            if(self._login_user_role) == 'admin':
                return self._userModel.find_by_username(username)
            else:
                self._latest_error = f'Login User {self._login_user_name} does not have sufficient rights to search user {username}'
                return -1
        except:
            self._latest_error = f'Error while trying to fetch user\'s details'
            return -1

    # This first checks if a user already exists with that username.
    # If it does, it populates latest_error and returns -1
    # If a user doesn't already exist, it'll insert a new document and return the same to the caller
    def insert(self, username, email, role):
        self._latest_error = ''
        try:
            if self._login_user_role == 'admin':
                user_document = self._userModel.insert(username, email, role)
                if user_document == -1:
                    self._latest_error = self._userModel.latest_error
                return user_document
            else:
                self._latest_error = f'Login User {self._login_user_name} does not have sufficient rights to insert user'
                return -1
        except:
            self._latest_error = f'Error while trying to insert user'
            return -1

    # User data can be deleted only by admin user
    def delete(self, username):
        self._latest_error = ''
        try:
            if self._login_user_role == 'admin':
                deleteAck = self._userModel.delete(username)
                if deleteAck is not True:
                    self._latest_error = self._userModel.latest_error
                return deleteAck
            else:
                self._latest_error = 'Logged in User does not have sufficient rights to delete user data'
                return -1
        except KeyError:
            self._latest_error = 'Logged in User does not have sufficient rights to delete user data'
            return -1
        except:
            self._latest_error = f'Error while trying to delete user'
            return -1

    # Users collection can be updated only by admin since no other user would have write access to users
    def update(self, username, param, value):
        self._latest_error = ''
        try:
            if self._login_user_role == 'admin':
                update_ack = self._userModel.update(username, param, value)
                if update_ack is not True:
                    self._latest_error = self._userModel.latest_error
                return update_ack
            else:
                self._latest_error = f'Logged in User does not have sufficient rights to update user'
                return -1
        except KeyError:
            self._latest_error = f'Logged in User does not have sufficient rights to update user'
            return -1
        except:
            self._latest_error = f'Error while trying to update user'
            return -1


# Device document contains device_id (String), desc (String), type (String - temperature/humidity)
# and manufacturer (String) fields
class DeviceModelService:
    def __init__(self,_login_user_role, _login_user_access):
        self._deviceModel = DeviceModel()
        self._latest_error = ''
        self._login_user_role = _login_user_role
        self._login_user_access = _login_user_access

    # Latest error is used to store the error string in case an issue.
    # It's reset at the beginning of a new function call
    @property
    def latest_error(self):
        return self._latest_error

    # Since device id should be unique in devices collection,
    # this provides a way to fetch the device document based on the device id
    def find_by_device_id(self, device_id):
        self._latest_error = ''
        try:
            if self._login_user_role == 'admin' or 'r' in self._login_user_access[device_id]:
                return self._deviceModel.find_by_device_id(device_id)
            else:
                self._latest_error = f'Logged in User does not have sufficient rights to search for device {device_id}'
                return -1
        except KeyError:
            self._latest_error = f'Logged in User does not have sufficient rights to search for device {device_id}'
            return -1

    # This first checks if a device already exists with that device id.
    # If it does, it populates latest_error and returns -1
    # If a device doesn't already exist, it'll insert a new document and return the same to the caller
    # Device can be inserted only by admin since no other user would have write access to device until it is created.
    def insert(self, device_id, desc, type, manufacturer):
        self._latest_error = ''
        try:
            if self._login_user_role == 'admin':
                device_document = self._deviceModel.insert(device_id, desc, type, manufacturer)
                if device_document == -1:
                    self._latest_error = self._deviceModel.latest_error
                return device_document
            else:
                self._latest_error = f'Logged in User does not have sufficient rights to insert device {device_id}'
                return -1
        except:
            self._latest_error = f'Error while trying to insert device data'
            return -1

    # Device can be updated only by admin or other user having write access to device.
    def update(self, device_id, param, value):
        self._latest_error = ''
        try:
            if self._login_user_role == 'admin' or 'w' in self._login_user_access[device_id]:
                update_ack = self._deviceModel.update(device_id, param, value)
                if (update_ack is not True):
                    self._latest_error = self._deviceModel.latest_error
                return update_ack
            else:
                self._latest_error = f'Logged in User does not have sufficient rights to update device {device_id}'
                return -1
        except KeyError:
            self._latest_error = f'Logged in User does not have sufficient rights to update device {device_id}'
            return -1
        except:
            self._latest_error = f'Error while trying to update device data'
            return -1

    # Device can be updated only by admin or other user having write access to device.
    def delete(self, device_id):
        self._latest_error = ''
        try:
            if self._login_user_role == 'admin' or 'w' in self._login_user_access[device_id]:
                delete_ack = self._deviceModel.delete(device_id)
                if (delete_ack is not True):
                    self._latest_error = self._deviceModel.latest_error
                return delete_ack
            else:
                self._latest_error = f'Logged in User does not have sufficient rights to delete device {device_id}'
                return -1
        except KeyError:
            self._latest_error = f'Logged in User does not have sufficient rights to delete device {device_id}'
            return -1
        except:
            self._latest_error = f'Error while trying to delete device data'
            return -1

# Weather data document contains device_id (String), value (Integer), and timestamp (Date) fields


class WeatherDataModelService:
    WEATHER_DATA_COLLECTION = 'weather_data'

    def __init__(self, _login_user_role, _login_user_access):
        self._weatherDataModel = WeatherDataModel()
        self._latest_error = ''
        self._login_user_role = _login_user_role
        self._login_user_access = _login_user_access

    # Latest error is used to store the error string in case an issue. Is reset at the beginning of a new function call
    @property
    def latest_error(self):
        return self._latest_error

    # Since device id and timestamp should be unique in weather_data collection,
    # this provides a way to fetch the data document based on the device id and timestamp
    def find_by_device_id_and_timestamp(self, device_id, timestamp):
        self._latest_error = ''
        try:
            if self._login_user_role == 'admin' or 'r' in self._login_user_access[device_id]:
                return self._weatherDataModel.find_by_device_id_and_timestamp(device_id, timestamp)
            else:
                self._latest_error = f'Logged in User does not have sufficient rights to search for weather data of device {device_id}'
                return -1
        except KeyError:
            self._latest_error = f'Logged in User does not have sufficient rights to search for weather data of device {device_id}'
            return -1
        except:
            self._latest_error = f'Error while trying to fetch weather data'
            return -1

    # This first checks if a data item already exists at a particular timestamp for a device id.
    # If it does, it populates latest_error and returns -1.
    # If it doesn't already exist, it'll insert a new document and return the same to the caller
    # Weather data can be inserted only by admin or user having write access to device.
    def insert(self, device_id, value, timestamp):
        self._latest_error = ''
        try:
            if self._login_user_role == 'admin' or 'w' in self._login_user_access[device_id]:
                weather_document = self._weatherDataModel.insert(device_id, value, timestamp)
                if weather_document == -1:
                    self._latest_error = self._weatherDataModel.latest_error
                return weather_document
            else:
                self._latest_error = f'Logged in User does not have sufficient rights to insert weather data for device {device_id}'
                return -1
        except KeyError:
            self._latest_error = f'Logged in User does not have sufficient rights to insert weather data for device {device_id}'
            return -1
        except:
            self._latest_error = f'Error while trying to insert weather data'
            return -1

    # Weather data can be deleted only by admin or user having write access to device.
    def delete(self, device_id, timestamp):
        self._latest_error = ''
        try:
            if self._login_user_role == 'admin' or 'w' in self._login_user_access[device_id]:
                delete_ack = self._weatherDataModel.delete(device_id, timestamp)
                if (delete_ack is not True):
                    self._latest_error = self._weatherDataModel.latest_error
                return delete_ack
            else:
                self._latest_error = f'Logged in User does not have sufficient rights to delete weather data for device {device_id}'
                return -1
        except KeyError:
            self._latest_error = f'Logged in User does not have sufficient rights to delete weather data for device {device_id}'
            return -1
        except:
            self._latest_error = f'Error while trying to delete weather data'
            return -1

    # Device weather data can be updated only by admin or other user having write access to device..
    def update(self, device_id, timestamp, param, value):
        self._latest_error = ''
        try:
            if self._login_user_role == 'admin' or 'w' in self._login_user_access[device_id]:
                update_ack = self._weatherDataModel.update(device_id, timestamp, param, value)
                if (update_ack is not True):
                    self._latest_error = self._weatherDataModel.latest_error
                return update_ack
            else:
                self._latest_error = f'Logged in User does not have sufficient rights to update weather data for {device_id}'
                return -1
        except KeyError:
            self._latest_error = f'Logged in User does not have sufficient rights to update weather data for {device_id}'
            return -1
        except:
            self._latest_error = f'Error while trying to update weather data'
            return -1

# User Device document contains user_id (String), access_type (Array) fields
# During object intialization for the logged in user, fetch the user's role and the corresponding device access,
# to be used later by device model and weather data model
class UserDeviceModelService:
    def __init__(self):
        self._userDeviceModel = UserDeviceModel()
        self._latest_error = ''

    # Latest error is used to store the error string in case an issue. Is reset at the beginning of a new function call
    @property
    def latest_error(self):
        return self._latest_error

    # Since user id should be unique in user_device_access collection,
    # this provides a way to fetch the user device access document based on the user id
    def find_access_by_username(self, username):
        self._latest_error = ''
        device_access = {}
        user_device_access = self._userDeviceModel.find_access_by_username(username)

        # Creates the device access list for the logged in user to determine read/write permissions on device
        try:
            if user_device_access['access'] is not None:
                for access in(user_device_access['access']):
                    device_access[access['device_id']] = access['access_type']
                return device_access
        except Exception:
            return device_access


# Daily Report document contains id as a combination of device ID and date from timestamp,
# and aggregated average, minimum and maximum data value fields


class DailyReportModelService:
    def __init__(self, _login_user_role):
        self._dailyReportModel = DailyReportModel()
        self._latest_error = ''
        self._login_user_role = _login_user_role

    # Latest error is used to store the error string in case an issue. Is reset at the beginning of a new function call
    @property
    def latest_error(self):
        return self._latest_error

    # Report aggregate data functionality included if admin wants to aggregate reports from weather data
    def aggregate(self):
        self._latest_error = ''
        try:
            if self._login_user_role == 'admin':
                datadoc = self._dailyReportModel.aggregate()
            else:
                self._latest_error = 'Logged in user does not have write to aggregate reports'
                return -1
        except :
            self._latest_error = 'Error while aggregating and inserting weather data into daily_reports'
            return -1

    # Fetching count of rows in report data functionality included to verify the count of rows in daily_reports.
    # If the service wants to be enables for all users, check for login user role can be removed
    def count_report_data(self):
        self._latest_error = ''
        try:
            if self._login_user_role == 'admin':
                datadoc = self._dailyReportModel.count_report_data()
                return datadoc
            else:
                self._latest_error = 'Logged in user does not have write to fetch reports related data'
                return -1
        except Exception:
            self._latest_error = 'Logged in user does not have write to fetch reports related data'
            return -1

    # Fetching report data functionality included if admin wants to fetch aggregated reports.
    # If the service wants to be enables for all users, check for login user role can be removed
    def fetch_report(self, device_id, start_date, end_date):
        self._latest_error = ''
        try:
            if self._login_user_role == 'admin':
                datadoc = self._dailyReportModel.fetch_report(device_id, start_date, end_date)
                return datadoc
            else:
                self._latest_error = 'Logged in user does not have write to fetch reports'
                return -1
        except Exception:
            self._latest_error = 'Error while fetching weather data daily_reports'
            return -1
