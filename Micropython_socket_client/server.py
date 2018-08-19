import socket
import time
import queue
from threading import Thread
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import csv

q=queue.Queue()

class server:
    def __init__(self):
        self.sock = None
        self.conn = None

    def connect(self):
        try:

            print("Trying to start socket server")
            self.sock = socket.socket()
            self.sock.bind(("", 14900))
            self.sock.listen(10)
            print("Done..")

        except Exception as er:
            if er.errno == 98:
                print("Socket already in use")
            self.sock = None
            time.sleep(3)
            print(er)


    def run(self):

        server = Thread(target=self.main)
        server.start()

        fig, ax = plt.subplots()
        scope = Scope(ax)

        ani = animation.FuncAnimation(fig, scope.update, emitter, interval=10,
                                      blit=True)

        scope = Thread(target=plt.show())
        scope.start()

        server.join()
        scope.join()



    def main(self):
        print("Start main server thread !")
        while True:
            try:
                while self.sock is None:
                    self.connect()
                self.conn, addr = self.sock.accept()
                self.conn.settimeout(3)  # timeout settings !
                if self.sock is None:
                    print("socket failed!!")
                data = self.conn.recv(2) # Receive two bytes
                if not data:
                    print("No data")
                    self.conn.close()
                data = int.from_bytes(data, byteorder='big')
                print("New data !!! = " + str(data)) # uncomment for socket data view !!!
                q.put(data) # put data to queue
                with open('result.csv', 'a') as csvfile:
                    writer = csv.writer(csvfile, delimiter=' ',
                                            quotechar=';', quoting=csv.QUOTE_MINIMAL)
                    writer.writerow([data, time.asctime(time.localtime(time.time()))])

            except Exception as er:
                if self.conn is not None:
                    self.conn.close()
                print("Exception " + str(er))
                # KeyboardInterrupt may be ???


class Scope(object):
    def __init__(self, ax, maxt=2, dt=0.02):
        self.ax = ax
        self.dt = dt
        self.maxt = maxt
        self.tdata = [0]
        self.ydata = [0]
        self.line = Line2D(self.tdata, self.ydata)
        self.ax.add_line(self.line)
        self.ax.set_ylim(-.1, 255) # Y range
        self.ax.set_xlim(0, self.maxt)

    def update(self, y):
        lastt = self.tdata[-1]
        if lastt > self.tdata[0] + self.maxt:  # reset the arrays
            self.tdata = [self.tdata[-1]]
            self.ydata = [self.ydata[-1]]
            self.ax.set_xlim(self.tdata[0], self.tdata[0] + self.maxt)
            self.ax.figure.canvas.draw()

        t = self.tdata[-1] + self.dt
        self.tdata.append(t)
        self.ydata.append(y)
        self.line.set_data(self.tdata, self.ydata)
        return self.line,


def emitter(p=0.03):

    while True:
        data = 0
        if q.empty():
            pass
        else:
            data = q.get(False)
            yield data

new = server()
new.run()
