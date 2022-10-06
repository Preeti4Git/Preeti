To execute, run main.py that demonstrates all the expected functionalities of the program, as can be checked from the console logs.

Points under consideration - 

1. Device registration acknowledgement (regconf) is received at device end where device subscribes to the topic specific to that particular device ID, else if it subscribes to devices/+/regconf, each device would receive the registration acknowledgement of all the numerous devices in the network.

2. In problem statement 2, I have returned the intensity and temperature only when the device switch status is ON, else it is irrelevant.

3. Demonstrated the light intensity and AC temperature validation (temperature out of bounds) as well in the problem statement 3.

4. This is the most secure design.
