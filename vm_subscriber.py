"""EE 250L Lab 04 Starter Code

Run vm_subscriber.py in a separate terminal on your VM."""

import paho.mqtt.client as mqtt
import time



def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    client.subscribe("mohaimen")

    client.subscribe("mohaimen/ultrasonicRanger")
    client.subscribe("mohaimen/button")

    client.message_callback_add("mohaimen/ultrasonicRanger", uRanger_callback)
    client.message_callback_add("mohaimen/button", button_callback)


def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))


#Custom callback to update the distance measurement read from the ultrasonic ranger on the rpi
def uRanger_callback(client, userdata, message):

    distance = str(message.payload, "utf-8")
    print("VM: " + distance + "cm")


#Custom callback to indicate button is pressed on rpi
def button_callback(client, userdata, message):

    button = str(message.payload, "utf-8")
    print(button)

if __name__ == '__main__':
    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()

    while True:
        
        time.sleep(1)
            

