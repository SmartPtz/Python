import serial.tools.list_ports
from queue import Queue
import time
from threading import Thread, Event

import sys

# parser for sms  https://github.com/adammck/pygsm/blob/master/pygsm/message/incoming.py ?
# man http://www.avislab.com/blog/wp-content/uploads/2015/10/Neoway_M590_AT_Command_Sets_V3.0.pdf

writer = Queue()
reader = Queue()

connection = None

def run():
    try:
        ControlledThread(target = ModemCLI)
        test = ControlledThread()

        GsmModem()
    except Exception as er:
        print("Main exception !", er)
    except KeyboardInterrupt as er:
        print("\nCtrl-C exit", er)
    finally:
        #server_thread.join()
        #raise KeyboardInterrupt()
        test.stop()
        sys.exit(1)

class ControlledThread(Thread):
    def __init__(self, interval=1, target=None):
        """ Constructor
        :type interval: int
        :param interval: Check interval, in seconds
        """
        self.interval = interval
        thread = Thread(target=target, args=())
        self._stop = Event()
        thread.daemon = True
        thread.start()

    def stop(self):
        print("thread stopped")
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()


class M590Exception(Exception):
    def __init__(self):
        pass


class Sim900Protocol():
    def __init__(self):
        pass


class M590Protocol():
    def __init__(self):
        self.network_name = None
        self.network_status = None
        self.signal_status = None
        self.info_commands = {'modem_ver':'ATI',
                              'model': 'AT+CGMM?',
                              'firmware': 'AT+GETVERS',
                              'status': 'AT + CPAS',
                              'network_status': 'AT+CREG?',
                              'imei': 'AT+CGSN',
                              'cimi': 'AT+CIMI',
                              'ccid': 'AT+CCID',
                              'rssi': 'AT+CSQ'}
        self.sms_commans = {}
        self.special_commands = {'cash_status': b'*100#'} # mean operator commands ..

    def get_cash_status(self):
        pass

    def get_modem_status(self, ser):
        pass

    def get_network_status(self):
        pass

    def get_sim_status(self):
        pass


class ModemCLI(M590Protocol):
    def __init__(self):
        super().__init__()
        print("Start modem CLI interface")
        while not connection:
            pass
        print("interface connected !")
        while connection:
            print ("Enter command or type help:")
            command = input()
            if self.info_commands.get(command):
                command = self.info_commands.get(command)
            if command == 'help':
                print("-----Neoway 590 HELP------")
                print("command = alias ")
                for command in self.info_commands.keys():
                    print("%s = %s" % (command, self.info_commands.get(command)))
            else:
                if len(command) > 0:
                    command = command + '\r'
                    command = command.encode()
                    writer.put_nowait(command)
                    time.sleep(1) # fix here !!!
                    while reader.empty() is False:
                        echo = reader.get()
                        print(echo)


class GsmModem(M590Protocol):
    def __init__(self):
        super().__init__()
        print("Start serial server")
        comlist = serial.tools.list_ports.comports()
        connected = []
        for element in comlist:
            connected.append(element.device)
        print("Connected COM ports: " + str(connected))
        while True:
            global connection
            connection = True
            try:
                with serial.Serial('/dev/ttyUSB0', 9600,
                                   timeout=1) as ser:  # TODO написать процедуру поиска устройства, перебора портов ?
                   while True:
                        line = ser.readline()
                        line = line.decode()
                        if len(line) > 0:
                            #reader.put_nowait(line)
                            reader.put(line)
                        if not writer.empty() and ser.out_waiting == 0:
                            ser.write(writer.get_nowait())
                        time.sleep(0.01)
            except serial.SerialException as er:
                connection = False
                print("Problem !", er)
                time.sleep(1)
                # print("Cant find device on port ! Try to reconnect")

if __name__ == '__main__':
    run()