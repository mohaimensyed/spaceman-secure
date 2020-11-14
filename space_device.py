
#LIBRARIES
import paho.mqtt.client as mqtt
import time
from pynput import keyboard



def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    client.subscribe("spaceman")

    client.subscribe("spaceman/detector")
    client.subscribe("spaceman/button")


    client.message_callback_add("spaceman/detector", uRanger_callback)
    client.message_callback_add("spaceman/button", button_callback)


#DEFAULT CALLBACK
def on_message(client, userdata, msg):
    print("System Locked")


#NOTIFY CLIENT OF ALIENS NEARBY
def uRanger_callback(client, userdata, message):

    distance = str(message.payload, "utf-8")
    print("Alien Nearby at " + distance + "cm")


#CALLBACK FOR WHEN BUTTON IS PRESSED AND ACCESS REQUESTED
def button_callback(client, userdata, message):

    password = str(message.payload, "utf-8")
    print("ACCESS REQUESTED")
    code = input("Enter password: ")

    if code == password:
        
        client.publish("spaceman/unlock", "ACCESS GRANTED")

    else:
        
        client.publish("spaceman/breach", "SYSTEM BREACHED")
        print("SYSTEM BREACHED")

if __name__ == '__main__':
    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()

    while True:
        
        time.sleep(1)
            

