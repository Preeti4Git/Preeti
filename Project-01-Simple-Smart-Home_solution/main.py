import time
from EdgeServer import Edge_Server
from LightDevice import Light_Device
from ACDevice import AC_Device
import os

WAIT_TIME = 0.25  

print("\nSmart Home Simulation started.")
# Creating the edge-server for the communication with the user

edge_server_1 = Edge_Server('edge_server_1')
time.sleep(WAIT_TIME)  

# Creating the light_device
print("Intitate the device creation and registration process." )
print("\nCreating the Light devices for their respective rooms.")
light_device_1 = Light_Device("light_1", "Kitchen")
time.sleep(WAIT_TIME)
light_device_2 = Light_Device("light_2", "BR1")
time.sleep(WAIT_TIME)
light_device_3 = Light_Device("light_3", "BR2")
time.sleep(WAIT_TIME)
light_device_4 = Light_Device("light_4", "Living")
time.sleep(WAIT_TIME)
light_device_5 = Light_Device("light_5", "Living")
time.sleep(WAIT_TIME)

# Creating the ac_device  
print("\nCreating the AC devices for their respective rooms. ")
ac_device_1 = AC_Device("ac_1", "BR1")
time.sleep(WAIT_TIME)
ac_device_2 = AC_Device("ac_2", "BR2")
time.sleep(WAIT_TIME)

print("\n<<<<<<<<<<<<<<IMPLEMENTATION OF PROBLEM STATEMENT 2a >>>>>>>>>>>>>>")
print("\nFETCH DEVICE STATUS FOR LIGHT TYPE DEVICES (FETCH BASED ON DEVICE TYPE)")
edge_server_1.get_status("deviceType", "LIGHT")
time.sleep(WAIT_TIME)
print("\nFETCH DEVICE STATUS FOR DEVICE ID ac_1 (BASED ON DEVICE ID)")
edge_server_1.get_status("deviceId", "ac_1")
time.sleep(WAIT_TIME)
print("\nFETCH DEVICE STATUS FOR DEVICES IN ROOM BR2 (BASED ON ROOM TYPE)")
edge_server_1.get_status("room", "BR2")
time.sleep(WAIT_TIME)
print("\nFETCH DEVICE STATUS FOR ALL DEVICES IN HOME")
edge_server_1.get_status("all", "all")
time.sleep(WAIT_TIME)

print("\n<<<<<<<<<<<<<<IMPLEMENTATION OF PROBLEM STATEMENT 2b >>>>>>>>>>>>>>")
print("\nSET DEVICE STATUS FOR LIGHT TYPE DEVICES (SET BASED ON DEVICE TYPE)")
edge_server_1.set_status("deviceType", "LIGHT", "ON")
time.sleep(WAIT_TIME)
print("\nSET DEVICE STATUS FOR DEVICE ID ac_1 (SET BASED ON DEVICE ID)")
edge_server_1.set_status("deviceId", "ac_1", "ON")
time.sleep(WAIT_TIME)
print("\nSET DEVICE STATUS FOR DEVICES IN ROOM BR2 (SET BASED ON ROOM TYPE)")
edge_server_1.set_status("room", "BR2", "ON")
time.sleep(WAIT_TIME)
print("\nSET DEVICE STATUS FOR ALL DEVICES IN HOME")
edge_server_1.set_status("all", "all", "OFF")
time.sleep(WAIT_TIME)
edge_server_1.set_status("all", "all", "ON")
time.sleep(WAIT_TIME)

print("\n<<<<<<<<<<<<<<IMPLEMENTATION OF PROBLEM STATEMENT 3a >>>>>>>>>>>>>>")
print("\nSET LIGHT INTENSITY BASED ON DEVICE ID)")
edge_server_1.set_light_intensity("deviceId", "light_2", "MEDIUM")
time.sleep(WAIT_TIME)
print("\nSET INTENSITY FOR LIGHT DEVICES IN LIVING ROOM (SET BASED ON ROOM TYPE)")
print("\n DEMONSTRATING INPUT VALIDATION AS WELL")
edge_server_1.set_light_intensity("room", "Living", "high")
time.sleep(WAIT_TIME)
edge_server_1.set_light_intensity("room", "Living", "HIGH")
time.sleep(WAIT_TIME)
print("\nSET NTENSITY OF LIGHT DEVICES FOR ALL DEVICES IN HOME")
edge_server_1.set_light_intensity("all", "all", "MEDIUM")
time.sleep(WAIT_TIME)

print("\n<<<<<<<<<<<<<<IMPLEMENTATION OF PROBLEM STATEMENT 3b >>>>>>>>>>>>>>")
print("\nSET AC TEMPERATURE BASED ON DEVICE ID)")
print("\n DEMONSTRATING INPUT VALIDATION AS WELL FOR TEMPERATURE OUT OF BOUNDS")
edge_server_1.set_ac_temperature("deviceId", "ac_2", "12")
time.sleep(WAIT_TIME)
print("\nSET AC TEMPERATURE IN LIVING ROOM (SET BASED ON ROOM TYPE)")
edge_server_1.set_ac_temperature("room", "BR1", "19")
time.sleep(WAIT_TIME)
print("\nSET AC TEMPERATURE FOR ALL AC DEVICES IN HOME")
edge_server_1.set_ac_temperature("all", "all", "18")
time.sleep(WAIT_TIME)


print("\nSmart Home Simulation stopped.")
edge_server_1.terminate()
