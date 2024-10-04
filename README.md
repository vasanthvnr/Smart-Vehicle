# Truck Project: Vehicle Communication
# Introduction
The Truck Project: Vehicle Communication is designed to enhance vehicle safety and communication using cameras, sensors, and real-time data analysis. This project leverages a Raspberry Pi to monitor and display important alerts, warnings, and footage for the driver, with a focus on preventing accidents, optimizing vehicle performance, and improving driver awareness.

# Key Features
Real-time Camera Footage: Display live camera feed from the front of the vehicle to monitor the road and communicate with other vehicles.
Alert System: Alert the driver based on specific events such as:
Left/Right turn alerts
Braking alerts
Overtaking warnings
Driver drowsiness detection
Object detection warnings
Engine part maintenance notifications
Weight Display: Always visible vehicle weight displayed on the left side of the screen.
Driver Fatigue Detection: Uses the MR688B Driver Fatigue Monitor to detect driver drowsiness and trigger an alert sound.
Sound Alerts: A buzzer system is implemented to give sound alerts based on different warning scenarios.
# Components
Raspberry Pi (Model 4B or higher recommended)
Camera Module for real-time footage capturing
MR688B Driver Fatigue Monitor for drowsiness detection
Sensors for object detection, engine part monitoring
LED Display (70% camera footage, 30% alerts)
# Hardware Setup
Connect the camera module to the Raspberry Pi using the CSI port.
Attach the MR688B Driver Fatigue Monitor to the driver's seat or dashboard.
Install proximity sensors for object detection in the front of the vehicle.
Set up the LED display to show camera footage and alerts.
Install speakers for sound alerts.
# Software Functionality
Camera Feed Display:

The camera captures the footage and displays it on the top 70% of the LED screen.
# Alert Messages and Buzzer:

Based on sensor inputs and driver actions, various alerts are displayed in the bottom 30% of the screen. These include:
Left/Right Turn Alerts: Press respective keys to display alert messages.
Overtaking Warning: Triggered when the driver attempts to overtake.
Driver Fatigue Alert: Triggered by the MR688B monitor when the driver shows signs of drowsiness.
Object Detection Warning: Press the O key to display "Object detected in front, go slow!"
Engine Repair Alert: Press the E key to display "It's time to repair the engine parts."
A buzzer will sound for urgent alerts, such as fatigue detection or proximity warnings.
Sound Alarm System:

Press the S key to initiate an alarm sound after 5 seconds, warning the driver of drowsiness or potential hazards.
Permanent Weight Display:

The vehicle’s weight is displayed on the left side of the screen permanently to ensure the driver is aware of the current load.


# finally the Source code is run by connecting the Hardware setup and upload the code given.
