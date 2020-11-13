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



#Custom callback for to turn the led on/off when the topic is updated
def unlock_callback(client, userdata, message):

    comm = str(message.payload, "utf-8")
    digitalWrite(buzzer, 1)
    digitalWrite(led_red, 0)

    time.sleep(0.1)
    digitalWrite(buzzer, 0)
    time.sleep(0.1)
    digitalWrite(buzzer, 1)
    time.sleep(0.1)
    digitalWrite(buzzer, 0)

    while True:

        setText_norefresh(comm)
        digitalWrite(led_green, 1)

        button_status = digitalRead(button)
        if button_status:
            break



#Custom callback to change display on lcd when the topic is updated
def breach_callback(client, userdata, message):

    comm = str(message.payload, "utf-8")
    
    setText_norefresh(comm)
    digitalWrite(led_green, 0)

    while True:

        digitalWrite(buzzer, 1)
        digitalWrite(led_red, 0)
        time.sleep(2)
        digitalWrite(buzzer, 0)
        digitalWrite(led_red, 0)


if __name__ == '__main__':
    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()

    while True:

        try:
        
            #takes a reading from ultrasonic sensor ever 1s and publishes in the ultrasonicRanger topic
            distance = ultrasonicRead(ultrasonic_ranger)
            digitalWrite(buzzer, 0)
            setText_norefresh("SYSTEM LOCKED")
            digitalWrite(led_red, 1)


            if distance <= 70:
        
                #Alert Host
                client.publish("spaceman/detector", distance)

                #when button is pressed, request access
                button_status = digitalRead(button)
                if button_status:

                    digitalWrite(buzzer, 1)
                    client.publish("spaceman/button", "ACCESS REQUESTED")
                    time.sleep(0.1)
                    digitalWrite(buzzer, 0)




            time.sleep(1)

        except KeyboardInterrupt:   # Turn LED off before stopping
            digitalWrite(led_red,0)
            digitalWrite(led_red,0)
            digitalWrite(buzzer,0)
            break
        
        except IOError:             # Print "Error" if communication error encountered
            print ("Error")
        
            

