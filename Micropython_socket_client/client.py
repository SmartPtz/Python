import socket
import time
import machine
adc = machine.ADC(0) #define 10 bits ADC GPIO

import network
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
if not wlan.isconnected():
    print('connecting to network...')
    wlan.connect('ZyxelSSA', 'staswifi')
    while not wlan.isconnected():
        pass
print('network config:', wlan.ifconfig())

while True:
    try:
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #conn = socket.socket()
        conn.connect(("192.168.0.33", 14900)) # define ip address and socket
        data = adc.read()  # read an analog value
        print('ADC = '+str(data))
        data = data.to_bytes(2, 'big')
        conn.send(data)
        time.sleep(1) # define time period
        conn.close()
    except Exception as er:
        print("Exception ! "+str(er))
        print("No server connection... Try to connect again")
        time.sleep(1) # reconnection timeout
        conn.close()



