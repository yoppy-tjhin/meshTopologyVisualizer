import re, serial
import list_comports

def init_serial(comPort=None, baudRate=115200):
    if comPort != None:
        ser = serial.Serial(comPort, baudRate, timeout=1)
        return ser

    # If comPort is not provided, use what are available, except 'COM1'. This is just the case in my PC.
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
        print (line)

        line = line.decode('utf-8')

        # The keyword 'MeshTopology', 'query-reply', etc. correspond to what are sent from the ESP serial
        if 'MeshTopology' in line :                                 # process lines containing 'MeshTopology'
            line_json = re.search(r"\s([{\[].*?[}\]])$", line)      # only take JSON strings
            #print (line_json.group(1))
            if line_json != None:                                   # check that json string extraction is successful
                return 'MeshTopology', line_json.group(1)           # return message-type, message-content
            else:
                return None, None                                   # if json string extraction is unsuccessful

        elif 'query-reply' in line:                                 # process lines containing 'query-reply'
            line_json = re.search(r"\s([{\[].*?[}\]])$", line)      # only take JSON strings
            if line_json != None:                                   # check that json string extraction is successful
                return 'query-reply', line_json.group(1)
            else:
                return None, None                                   # if json string extraction is unsuccessful

        elif 'myFreeMemory-reply' in line:
            #line_json = re.search(r"\s([{\[].*?[}\]])$", line)  # only take JSON strings
            #if line != None:  # check if it is a JSON string
            return 'myFreeMem', line
            #else:
            #    return None, None  # when it is not a JSON string

        else:
            return None, None
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

