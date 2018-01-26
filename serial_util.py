import re, serial, time, threading
import list_comports

def init_serial(comPort=None, baudRate=115200):
    if comPort != None:
        ser = serial.Serial(comPort, baudRate, timeout=1)
        return ser

    # below is implicitly elseif
    for port in list_comports.serial_ports():
        if port != 'COM1':
            comPort = port                  # the first found port other than COM1
            ser = serial.Serial(comPort, baudRate, timeout=1)
            return ser
    return None
    # TODO: if serial port not found

# def getSerialSetting():
#     return 'Port: ' + str(self.comPort) + '. Baud rate: ' + str(self.baudRate)

# return JSON Strings only
def read_json_string(ser):
    # UNCOMMENT 'while' for use in threading mode
    #while True:
        #lock = threading.Lock()
        #lock.acquire()
        line = ser.readline()  # read a '\n' terminated line
        #print (line)
        #lock.release()
        print (line)
        if line :                       # check if the serial bytes is not empty
            line_json = re.search(r"\s([{\[].*?[}\]])$", line.decode('utf-8'))      # only take JSON strings
            if line_json != None:       # check if it is a JSON string
                return line_json.group(1)
            else:
                return None             # when it is not a JSON string
        else:
            return None
            # if (line_json != None):
            #     lock.acquire()
            #     print( line_json.group(1) )
            #     lock.release()
        #time.sleep(0.5)


# def run_serial_thread(self):
#     #serial_port = serial.Serial(self.comPort, self.baudRate, timeout=0)
#     #thread = threading.Thread(target=self.read_json_string, args=(serial_port,))     # example, with args
#     thread = threading.Thread(target=self.read_json_string())
#     thread.start()

# call with:
# Serial() --> default COM port: first available PORT other than COM1. default baudRate: 115200
# or Serial(comport = 'COM12', baudRate = 115200)
# or Serial (comport = 'COM12')
# or Serial (baudRate = '115200)
# ser = Serial()
#ser.run_serial_thread()

#for standalone testing
# while True:
#     if (ser.ser.is_open==0):
#         ser.ser.open()
#     jsonString = ser.read_json_string()
#     if jsonString != None:
#         print (jsonString)
#         print(ser.ser.inWaiting())
#         ser.ser.close()
#     time.sleep(0.3)

