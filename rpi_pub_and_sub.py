"""EE 250L Lab 04 Starter Code

Run rpi_pub_and_sub.py on your Raspberry Pi."""

import paho.mqtt.client as mqtt
import time
import grovepi
from grovepi import *
from grove_rgb_lcd import *

button = 6
ultrasonic_ranger = 3
led_green = 4
led_red = 2
buzzer = 5

setRGB(0,255,0)

pinMode(led_green, "OUTPUT")
pinMode(led_red, "OUTPUT")
pinMode(buzzer, "OUTPUT")
pinMode(button, "INPUT")
pinMode(ultrasonic_ranger, "INPUT")

#on connect the rpi will subscribe to the led and lac topics
def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))
    client.subscribe("spaceman")

    client.subscribe("spaceman/unlock")
    client.subscribe("spaceman/breach")
    client.message_callback_add("spaceman/unlock", unlock_callback)
    client.message_callback_add("spaceman/breach", breach_callback)

#default callback
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))
    setText("SYSTEM LOCKED")
    digitalWrite(led_red, 1)


#Custom callback for to turn the led on/off when the topic is updated
def unlock_callback(client, userdata, message):

    comm = str(message.payload, "utf-8")

    digitalWrite(led_green, 1)
    setText(comm)


#Custom callback to change display on lcd when the topic is updated
def breach_callback(client, userdata, message):

    comm = str(message.payload, "utf-8")

    digitalWrite(led_red, 1)
    setText(comm)


if __name__ == '__main__':
    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()

    while True:

        #takes a reading from ultrasonic sensor ever 1s and publishes in the ultrasonicRanger topic
        distance = ultrasonicRead(ultrasonic_ranger)

        if distance <= 70:
        
            #Alert Host
            client.publish("spaceman/detector", distance)

            #when button is pressed, request access
            button_status = digitalRead(button)
            if button_status:

                client.publish("spaceman/button", "Button Pressed")

        else:
            
            client.publish("spaceman")


        time.sleep(1)
            

