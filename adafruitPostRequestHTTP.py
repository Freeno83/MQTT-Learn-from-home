#Witten by Nick Robinson, 06Apr20
#This code allows you to switch a relay on/off via HTTP post
#Total time that the request.post action takes is displayed for reference

import requests
import time

"""If using Adafruit IO onoff example, just enter your userName and aoiKey"""
broker = 'https://io.adafruit.com/api/v2'
userName = ''
feed = 'onoff'
url = f'{broker}/{userName}/feeds/{feed}/data'
aioKey = ''

messageCount = 0
totalTime = 0

while True:
    """Get input from the user"""
    value = input('Enter ON or OFF (q to quit): ')
    value = value.upper()
    
    if (value != 'ON') and (value != 'OFF') and (value != 'Q'):
        print('Invalid input')
        continue
    
    if value == 'Q':
        aveTime = totalTime / messageCount
        print(f'Average {aveTime:.3f} seconds for {messageCount} transactions')
        break 

    """Parameters are the aioKey and the value to be updated"""
    payload = {'x-aio-key': aioKey, 'value': value}

    """Send the post request and compute response time"""
    startTime = time.time()
    r = requests.post(url, data = payload)
    transTime = time.time() - startTime
    messageCount += 1
    totalTime += transTime

    """Display the HTTP status code and response time"""
    print(f'HTTP status code: {r.status_code}')
    print(f'Response time: {transTime:.3f} seconds')

    """If there were no errors, display the returned value"""
    if(r.status_code == 200):
        data = r.json()
        print(f'Relay Status: {data["value"]}\n')
