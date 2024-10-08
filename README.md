# SPACEMAN SECURE

SPACEMAN SECURE is a security system that alerts subscribed clients when someone or something is detected within close proximity of the system. It also detects potential intruders trying to access the system.

## Features

- Proximity detection using an ultrasonic ranger
- Access request system with a physical button
- Password-based access control
- Alert system for unauthorized access attempts
- Visual feedback using LED lights and LCD display
- Audio feedback using a buzzer

## Video Demo

Check out our video demonstration of SPACEMAN SECURE in action:

[SPACEMAN SECURE Demo Video](https://drive.google.com/file/d/REPLACE_THIS_WITH_ACTUAL_FILE_ID/view?usp=sharing)

## Components

- Raspberry Pi Model 3B+
- GrovePi+
- LCD RGB Display screen
- Two LED lights (Red and Blue)
- Button
- Buzzer
- Ultrasonic Ranger

## Communication

The system uses the MQTT Pub/Sub Protocol for communication between nodes, with "eclipse.usc.edu" as the broker.

## Functionality

1. The system starts in a locked state with a green LCD display showing "SYSTEM LOCKED".
2. The ultrasonic ranger continuously monitors for nearby objects.
3. When an object is detected within 50cm, all subscribed clients are notified.
4. Pressing the button sends an access request to the clients.
5. Clients must enter the correct passcode to grant access.
6. If access is granted:
   - The blue LED turns on
   - The LCD display turns blue and shows "ACCESS GRANTED"
7. If access is denied:
   - All clients are notified of a system breach
   - The red LED flashes
   - The buzzer sounds an alarm
   - The LCD display turns red and shows "SYSTEM BREACHED"

## Files

1. `rpi_space_secure.py`: Script for the Raspberry Pi device
2. `space_device.py`: Script for the client devices

## Setup and Usage

1. Connect all the hardware components to the Raspberry Pi according to the pin configurations in the script.
2. Install the required libraries:
   ```
   pip install paho-mqtt grovepi grove_rgb_lcd
   ```
3. Run `rpi_space_secure.py` on the Raspberry Pi.
4. Run `space_device.py` on each client device.

## Limitations and Future Improvements

- The system currently faces i2c race conditions.
- It cannot detect which specific device entered the wrong passcode.
- Time logging for access requests is not implemented.

Future improvements could include:
- Assigning unique serial numbers to each subscribed device
- Implementing time logs for access requests
- Creating a database to store client information and access logs

## Author

Mohaimen Syed

## Note

This project was created as a demonstration of MQTT protocol usage and IoT security concepts. It is not intended for production use without further security enhancements.
