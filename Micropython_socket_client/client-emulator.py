import socket
import time
import random

while True:
    try:
        conn = socket.socket()
        conn.connect(("127.0.0.1", 14900)) # define ip address and socket
        data = random.randint(0, 255)
        data = data.to_bytes(2, byteorder='big')
        conn.send(data)
        time.sleep(1)
        # conn.close()
    except Exception as er:
        print("exception = " + str(er.errno))
        if er.errno == 111:
            print("No server connection... Try to connect again")
        else:
            print("Error =" + str(er.errno))
            #conn.close()
        time.sleep(3) # reconnection timeout



