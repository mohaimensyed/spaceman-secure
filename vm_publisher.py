"""EE 250L Lab 04 Starter Code

Run vm_publisher.py in a separate terminal on your VM."""

import paho.mqtt.client as mqtt
import time
from pynput import keyboard

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))



def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

#publishes to the led and lcd topics when the keys are pressed
def on_press(key):
    try: 
        k = key.char # single-char keys
    except: 
        k = key.name # other keys
    
    if k == 'w':
        client.publish("mohaimen/lcd", "w")

    elif k == 'a':
        client.publish("mohaimen/led", "LED_ON")
        client.publish("mohaimen/lcd", "a")

    elif k == 's':
        client.publish("mohaimen/lcd", "s")

    elif k == 'd':
        client.publish("mohaimen/led", "LED_OFF")
        client.publish("mohaimen/lcd", "d")


if __name__ == '__main__':
    #setup the keyboard event listener
    lis = keyboard.Listener(on_press=on_press)
    lis.start() # start to listen on a separate thread

    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()

    while True:

        time.sleep(1)
            

