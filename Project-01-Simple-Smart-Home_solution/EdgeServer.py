import collections
import json
import time
import paho.mqtt.client as mqtt

HOST = "localhost"
PORT = 1883     
WAIT_TIME = 0.25
ROOM_TYPES = ['Kitchen','BR1','BR2','Living']
DEVICE_TYPES = ['LightDevice','ACDevice']

# Reading the configuration file
f = open("config.json")
config = json.loads(f.read())
f.close()

class Edge_Server:
    
    def __init__(self, instance_name):
        
        self._instance_id = instance_name
        self.client = mqtt.Client(self._instance_id)
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.client.connect(host=config["broker_host"], port=config["broker_port"], keepalive=60)
        self.client.loop_start()
        self._registered_list = []
        self.roomwise = collections.defaultdict(list)
        self.device_type_wise  = collections.defaultdict(list)
        self.roomwise_light_devices = collections.defaultdict(list)
        self.roomwise_ac_devices = collections.defaultdict(list)

    # Terminating the MQTT broker and stopping the execution
    def terminate(self):
        self.client.disconnect()
        self.client.loop_stop()

    # Connect method to subscribe to various topics.     
    def _on_connect(self, client, userdata, flags, result_code):
        print("EdgeServer client connected with result code " + str(result_code))
        client.subscribe("devices/reg/+")
        print("EdgeServer subscribes to devices/reg/+ for devices registration requests")
        client.subscribe("devices/status/+")
        print("EdgeServer subscribes to devices/status/+ to find status of devices")
        
    # method to process the recieved messages and publish them on relevant topics 
    # this method can also be used to take the action based on received commands
    def _on_message(self, client, userdata, msg):
        if msg.topic.split("/")[1] == "reg":
            register_device_id = msg.topic.split("/")[2]
            if register_device_id not in self._registered_list:
                self._registered_list.append(register_device_id)
                print(self.get_registered_device_list())
                regconf_topic = "devices/regconf/"+register_device_id
                message = register_device_id
                print("regconf being sent for "+message+" from EdgeServer to the topic "+regconf_topic)
                self.client.publish(regconf_topic, json.dumps(message))
                room = json.loads(msg.payload)["room_type"]
                if room not in self.roomwise:
                    self.roomwise[room] = register_device_id
                    print("roomwise devices list ")
                    print(self.roomwise)
                else:
                    devices = []
                    devices.append(self.roomwise[room])
                    devices.append(register_device_id)
                    self.roomwise[room] = devices
                    print("roomwise devices list ")
                    print(self.roomwise)
                device_type = json.loads(msg.payload)["device_type"]
                print (" device_type "+ device_type)
                self.device_type_wise[device_type].append(register_device_id)
                print("device_type_wise devices list ")
                print(self.device_type_wise)
                if json.loads(msg.payload)["device_type"] == "LIGHT":
                    self.roomwise_light_devices[json.loads(msg.payload)["room_type"]].append(register_device_id)
                    print(" light list >>> ")
                    print(self.roomwise_light_devices)
                elif json.loads(msg.payload)["device_type"] == "AC":
                    self.roomwise_ac_devices[json.loads(msg.payload)["room_type"]].append(register_device_id)
                    print(" ac list >>> ")
                    print(self.roomwise_ac_devices)
            else:
               print("Device "+register_device_id+" is already registered")
        elif msg.topic.split("/")[1] == "status":
            print("EdgeServer received Device status for the device "+msg.topic.split("/")[2]+" as "+str(msg.payload))

    # Filtering the publish topics based on the diiferent type of request recieved. 
    def _filter_status_topics(self, param_type, param_value):
        if param_type == "deviceId":
            deviceIdlist = []
            deviceIdlist.append(param_value)
            return deviceIdlist
        elif param_type == "deviceType":
            return self.device_type_wise[param_value]
        elif param_type == "room":
            return self.roomwise[param_value]
        elif param_type == "all":
            return self._registered_list

    def _filter_light_intensity_topics(self, param_type, param_value):
        if param_type == "deviceId":
            deviceIdlist = []
            deviceIdlist.append(param_value)
            return deviceIdlist
        elif param_type == "room":
            return self.roomwise_light_devices[param_value]
        elif param_type == "all":
            return self.device_type_wise["LIGHT"]

    def _filter_ac_temp_topics(self, param_type, param_value):
        if param_type == "deviceId":
            deviceIdlist = []
            deviceIdlist.append(param_value)
            return deviceIdlist
        elif param_type == "room":
            return self.roomwise_ac_devices[param_value]
        elif param_type == "all":
            return self.device_type_wise["AC"]

    # Returning the current registered list
    def get_registered_device_list(self):
        return self._registered_list

    # Getting the status for the connected devices
    def get_status(self, paramtype, paramvalue): #deviceId,deviceType,room,all):
        device_id_list = self._filter_status_topics(paramtype, paramvalue)
        print(device_id_list)
        for device_id in device_id_list:
            print("Publishing to the topic " +"devices/getstatus/" + device_id + " for getting device status")
            self.client.publish("devices/getstatus/" + device_id)
            time.sleep(WAIT_TIME)


    # Controlling and performing the operations on the devices
    # based on the request received
    def set_status(self, paramtype, paramvalue, status):
        device_id_list = self._filter_status_topics(paramtype, paramvalue)
        print(device_id_list)
        for device_id in device_id_list:
            print("Publishing to the topic " + "devices/cmd/" + device_id + " for setting device status")
            message = {}
            message["device_id"] = device_id
            message["status"] = status
            self.client.publish("devices/cmd/" + device_id, json.dumps(message))
            time.sleep(WAIT_TIME)

    # Controlling and performing the operations on the devices
    # based on the request received
    def set_light_intensity(self, paramtype, paramvalue, intensity):
        device_id_list = self._filter_light_intensity_topics(paramtype, paramvalue)
        print(device_id_list)
        for device_id in device_id_list:
            print("Publishing to the topic cmdctrl for setting light intensity")
            print(device_id)
            message = {}
            message["device_id"] = device_id
            message["intensity"] = intensity
            self.client.publish("devices/cmdctrl/" + device_id, json.dumps(message))
            time.sleep(WAIT_TIME)

    # Controlling and performing the operations on the devices
    # based on the request received
    def set_ac_temperature(self, paramtype, paramvalue, temp):
        device_id_list = self._filter_ac_temp_topics(paramtype, paramvalue)
        print(device_id_list)
        for device_id in device_id_list:
            print("Publishing to the topic cmdctrl for setting ac temp")
            print(device_id)
            message = {}
            message["device_id"] = device_id
            message["temp"] = temp
            self.client.publish("devices/cmdctrl/" + device_id, json.dumps(message))
            time.sleep(WAIT_TIME)
