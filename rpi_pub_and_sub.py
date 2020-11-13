"""EE 250L Lab 04 Starter Code

Run rpi_pub_and_sub.py on your Raspberry Pi."""

import paho.mqtt.client as mqtt
import time
import grovepi
from grovepi import *
from grove_rgb_lcd import *

button = 2
ultrasonic_ranger = 3
led = 4

setRGB(0,255,0)

pinMode(led, "OUTPUT")
pinMode(button, "INPUT")
pinMode(ultrasonic_ranger, "INPUT")

#on connect the rpi will subscribe to the led and lac topics
def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))
    client.subscribe("mohaimen")

    client.subscribe("mohaimen/led")
    client.subscribe("mohaimen/lcd")
    client.message_callback_add("mohaimen/led", led_callback)
    client.message_callback_add("mohaimen/lcd", lcd_callback)

#default callback
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))


#Custom callback for to turn the led on/off when the topic is updated
def led_callback(client, userdata, message):

    comm = str(message.payload, "utf-8")

    if comm == 'LED_ON':
        digitalWrite(led, 1)

    if comm == 'LED_OFF':
        digitalWrite(led, 0)

#Custom callback to change display on lcd when the topic is updated
def lcd_callback(client, userdata, message):

    comm = str(message.payload, "utf-8")
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
        client.publish("mohaimen/ultrasonicRanger", distance)

        #when button is pressed, publishes the message on the button topic
        button_status = digitalRead(button)
        if button_status:
            client.publish("mohaimen/button", "Button Pressed")

        time.sleep(1)
            

