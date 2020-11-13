"""EE 250L Lab 04 Starter Code

Run rpi_pub_and_sub.py on your Raspberry Pi."""

import paho.mqtt.client as mqtt
import time
import grovepi
from grovepi import *
from grove_rgb_lcd import *
import threading 

lock = threading.Lock()

def protect(fn):
    with lock:
        return fn()

for BUS in [grovepi.bus,grove_rgb_lcd.bus]:
    for k in dir(BUS):
        if sum(map(lambda x: x in k,['read','write','i2c'])):
            fn = BUS.__getattribute__(k)
            BUS.__setattr__(k,fn)



button = 6
ultrasonic_ranger = 3
led_blue = 4
led_red = 2
buzzer = 5
breach = False


pinMode(led_blue, "OUTPUT")
pinMode(led_red, "OUTPUT")
pinMode(buzzer, "OUTPUT")
pinMode(button, "INPUT")
pinMode(ultrasonic_ranger, "INPUT")

with lock:
    setRGB(0,255,0)
    digitalWrite(buzzer, 0)
    setText_norefresh("SYSTEM LOCKED")
    digitalWrite(led_red, 1)
    digitalWrite(led_blue, 0)

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
    with lock:
        digitalWrite(buzzer, 1)
        digitalWrite(led_red, 0)

    time.sleep(0.1)
    digitalWrite(buzzer, 0)
    time.sleep(0.1)
    digitalWrite(buzzer, 1)
    time.sleep(0.1)
    digitalWrite(buzzer, 0)

    with lock:
        setRGB(0,100,255)
        setText_norefresh(comm)
        digitalWrite(led_blue, 1)





#Custom callback to change display on lcd when the topic is updated
def breach_callback(client, userdata, message):

    comm = str(message.payload, "utf-8")
    with lock:
        setRGB(255, 0, 0)
        setText_norefresh(comm)
        digitalWrite(led_blue, 0)
        digitalWrite(led_red, 1)
    

    breach = True



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
            with lock:
                distance = ultrasonicRead(ultrasonic_ranger)



            if distance <= 50:
        
                #Alert Host
                client.publish("spaceman/detector", distance)

                #when button is pressed, request access
                with lock:
                    button_status = digitalRead(button)
                if button_status:
                    with lock:
                        digitalWrite(buzzer, 1)
                    client.publish("spaceman/button", "ACCESS REQUESTED")
                    time.sleep(0.1)
                    with lock:
                        digitalWrite(buzzer, 0)

            if breach == True:
                while True:
                    with lock:
                        digitalWrite(buzzer, 1)
                        digitalWrite(led_red, 1)
                    time.sleep(2)
                    with lock:
                        digitalWrite(buzzer, 0)
                        digitalWrite(led_red, 0)


            time.sleep(1)

        
        except KeyboardInterrupt:   # SHUTS OFF ALL OUTPUT
            digitalWrite(led_red,0)
            digitalWrite(led_blue,0)
            digitalWrite(buzzer,0)
            break
        
        except IOError:             # PrintS "Error" if communication error encountered
            print ("Error")
        
            

