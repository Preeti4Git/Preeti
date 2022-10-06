
import json
import paho.mqtt.client as mqtt


HOST = "localhost"
PORT = 1883

# Reading the configuration file
f = open("config.json")
config = json.loads(f.read())
f.close()
    
class AC_Device():
    
    _MIN_TEMP = 18  
    _MAX_TEMP = 32

    def __init__(self, device_id, room):
        
        self._device_id = device_id
        self._room_type = room
        self._temperature = 22
        self._device_type = "AC"
        self._device_registration_flag = False
        self.client = mqtt.Client(self._device_id)
        self.client.on_connect = self._on_connect  
        self.client.on_message = self._on_message  
        self.client.on_disconnect = self._on_disconnect  
        self.client.connect(host=config["broker_host"], port=config["broker_port"], keepalive=60)

        self.client.loop_start()  
        self._register_device(self._device_id, self._room_type, self._device_type)
        self._switch_status = "OFF"

    # calling registration method to register the device
    def _register_device(self, device_id, room_type, device_type):
        print("Registering device " + device_id)
        topic = "devices/reg/" + device_id
        message = {}
        message["room_type"] = room_type
        message["device_type"] = device_type
        self.client.publish(topic, json.dumps(message))

    # Connect method to subscribe to various topics. 
    def _on_connect(self, client, userdata, flags, result_code):
        print("ACDevice Connected with result code " + str(result_code))
        client.subscribe("devices/regconf/" + self._device_id)
        print("ACDevice subscribes to devices/regconf/" + self._device_id)
        client.subscribe("devices/getstatus/" + self._device_id)
        print("ACDevice subscribes to devices/getstatus/" + self._device_id)
        client.subscribe("devices/cmd/" + self._device_id)
        print("ACDevice subscribes to devices/cmd/" + self._device_id)
        client.subscribe("devices/cmdctrl/" + self._device_id)
        print("ACDevice subscribes to devices/cmdctrl/" + self._device_id)

    # method to process the recieved messages and publish them on relevant topics 
    # this method can also be used to take the action based on received commands
    def _on_message(self, client, userdata, msg):
        if msg.topic.split("/")[1] == "regconf":
            print("Reg Conf received for successful registration of AC device " + msg.topic.split("/")[2])
        elif msg.topic.split("/")[1] == "getstatus":
            print("In ACDevice publishing status as " + self._get_switch_status() + " to the topic " +
                  "devices/status/" + msg.topic.split("/")[2])
            self._publish_status(msg)
        elif msg.topic.split("/")[1] == "cmd":
            desired_status = json.loads(msg.payload)["status"]
            print("In ACDevice got set status command as " + desired_status + " on the topic " +
                  "devices/cmd/" + msg.topic.split("/")[2])
            self._set_switch_status(desired_status)
            self._publish_status(msg)
        elif msg.topic.split("/")[1] == "cmdctrl":
            desired_temp = json.loads(msg.payload)["temp"]
            print("In ACDevice got set temp command as " + desired_temp + " on the topic " +
                  "devices/cmdctrl/" + msg.topic.split("/")[2])
            if int(desired_temp) >= self._MIN_TEMP and int(desired_temp) <= self._MAX_TEMP :
                self._set_temperature(desired_temp)
                self._publish_status(msg)
            else :
                message = {}
                message["error"] = "Temperature out of bounds!!"
                self.client.publish("devices/status/" + msg.topic.split("/")[2], json.dumps(message))

    # Getting the current switch status of devices 
    def _get_switch_status(self):
        return self._switch_status

    # Setting the the switch of devices
    def _set_switch_status(self, switch_state):
        self._switch_status = switch_state

    # Getting the temperature for the devices
    def _get_temperature(self):
        return self._temperature

    # Setting up the temperature of the devices
    def _set_temperature(self, temperature):
        self._temperature = temperature

    def _publish_status(self, msg):
        message = {}
        message["device_id"] = msg.topic.split("/")[2]
        message["status"] = self._get_switch_status()
        if self._get_switch_status() == "ON":
            message["temp"] = self._get_temperature()
        self.client.publish("devices/status/" + msg.topic.split("/")[2], json.dumps(message))

    # Performing disconnect operation
    def _on_disconnect(self, client, userdata, result_code):
        self.client.loop_stop()
        print(f'Disconnected {self._device_type}_MQTT_instance "{self._device_id}" with result code={str(result_code)}')
        
