"""EE 250L Lab 04 Starter Code

Run vm_subscriber.py in a separate terminal on your VM."""

import paho.mqtt.client as mqtt
import time
from pynput import keyboard

password = "aliens=bruins"


def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    client.subscribe("spaceman")

    client.subscribe("spaceman/detector")
    client.subscribe("spaceman/button")

    client.message_callback_add("spaceman/detector", uRanger_callback)
    client.message_callback_add("spaceman/button", button_callback)


def on_message(client, userdata, msg):
    print("System Locked")


#Custom callback to update the distance measurement read from the ultrasonic ranger on the rpi
def uRanger_callback(client, userdata, message):

    distance = str(message.payload, "utf-8")
    print("Alien Nearby at " + distance + "cm")


#Custom callback to indicate button is pressed on rpi
def button_callback(client, userdata, message):

    button = str(message.payload, "utf-8")
    print(button)
    code = input("Enter password: ")

    if code is password:
        
        client.publish("spaceman/unlock", "ACCESS GRANTED")

    else:
        
        client.publish("spaceman/breach", "SYSTEM BREACHED")

if __name__ == '__main__':
    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()

    while True:
        
        time.sleep(1)
            

