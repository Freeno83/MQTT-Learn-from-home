#Witten by Nick Robinson, 06Apr20
#This code allows you to publish on/off messages to an MQTT broker
#After every new command is published the current subscribed value will be displayed
#Total time from publish start to subscribed message received is also displayed

import paho.mqtt.client as mqtt 
import time

"""If using Adafruit IO onoff example, just enter your userName and aoiKey"""
broker = 'io.adafruit.com'
userName = ' '
feed = 'onoff'
path = f'{userName}/feeds/{feed}'
aioKey = ' '

messageCount = 0
totalTime = 0


def on_connect(client, userdata, flags, rc):
    """Upon connection, subscribe to the path and call publishValue"""

    print(f'Connected to {broker} with result code {rc}')
    print(f'Subscribing to topic: {path}\n')
    client.subscribe(path)
    publishValue()


def on_disconnect(client, userdata, rc):
    """Notify the user that the connection has been closed"""

    print(f'Disconnected from {broker} with result code {rc}')

def on_message(client, userdata, message):
    """Display received messages and transaction time, call publishValue"""

    endTime = time.time()
    global totalTime
    
    print("Relay was set to: ", str(message.payload.decode("utf-8")))
    transTime = endTime - startTime
    totalTime += transTime
    
    print(f'Transaction time: {transTime:.3f} seconds\n')
    publishValue()

def publishValue():
    """Get input values from user text entry"""

    global startTime
    global messageCount

    while True:
        value = input('Enter ON or OFF (q to quit): ')
        value = value.upper()
    
        if (value != 'ON') and (value != 'OFF') and (value != 'Q'):
            print('Invalid input')
        else:
            break
    
    if value == 'Q':
        print(f'\nAverage {totalTime/messageCount:.3f} secoonds for {messageCount} transactions')
        client.disconnect()
        
    startTime = time.time()
    client.publish(path, value)
    messageCount += 1 

"""Create a client instance, set call backs, and conenct to broker"""
client = mqtt.Client()
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

client.username_pw_set(userName, aioKey)
client.connect(broker)
client.loop_forever()






