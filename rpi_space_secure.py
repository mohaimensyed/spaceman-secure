
#LIBRARIES 
import paho.mqtt.client as mqtt
import time
import grovepi
from grovepi import *
from grove_rgb_lcd import *

#PASSWORD USED TO GRANT ACCESS
password = "aliensgotoucla"

#ALL INPUT AND OUTPUT DEVICES
led_red = 2
ultrasonic_ranger = 3
led_blue = 4
buzzer = 5
button = 6

pinMode(led_blue, "OUTPUT")
pinMode(led_red, "OUTPUT")
pinMode(buzzer, "OUTPUT")
pinMode(button, "INPUT")
pinMode(ultrasonic_ranger, "INPUT")

#INITIAL STATE:
setRGB(0,255,0)
digitalWrite(buzzer, 0)
setText_norefresh("SYSTEM LOCKED")
digitalWrite(led_red, 0)
digitalWrite(led_blue, 0)

#ON CONNECT SUBSCRIBES TO UNLOCK AND BREACH TOPICS
def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))
    client.subscribe("spaceman")

    client.subscribe("spaceman/unlock")
    client.subscribe("spaceman/breach")
    client.message_callback_add("spaceman/unlock", unlock_callback)
    client.message_callback_add("spaceman/breach", breach_callback)

#DEFAULT CALLBACK
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))


#CALLBACK USED WHEN DEVICE IS UNLOCKED
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

    setRGB(0,100,255)
    setText_norefresh(comm)
    digitalWrite(led_blue, 1)



#CALLBACK USED WHEN THERE IS A BREACH
def breach_callback(client, userdata, message):

    comm = str(message.payload, "utf-8")

    setRGB(255, 0, 0)
    setText_norefresh(comm)
    digitalWrite(led_blue, 0)
    digitalWrite(led_red, 1)
    

    while True:
        digitalWrite(buzzer, 1)
        digitalWrite(led_red, 1)
        time.sleep(2)
        digitalWrite(buzzer, 0)
        digitalWrite(led_red, 0)
        time.sleep(2)



if __name__ == '__main__':
    
    #CREATES AN MQTT CLIENT AND CONNECTS TO eclipse.usc.edu at port 11000
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()

    while True:

        try:
        
            #TAKES READING FROM RANGER AND REPORTS IF OBJECT IS WITHIN 50cm
            distance = ultrasonicRead(ultrasonic_ranger)

            if distance <= 50:
        
                #Alert Host
                client.publish("spaceman/detector", distance)

                #when button is pressed, request access
                button_status = digitalRead(button)
                if button_status:
                    digitalWrite(buzzer, 1)
                    client.publish("spaceman/button", password)
                    time.sleep(0.1)
                    digitalWrite(buzzer, 0)


            time.sleep(1)

        
        except KeyboardInterrupt:   # SHUTS OFF ALL OUTPUT
            digitalWrite(led_red,0)
            digitalWrite(led_blue,0)
            digitalWrite(buzzer,0)
            break
        
        except IOError:             # PrintS "Error" if communication error encountered
            print ("Error")
        
            

