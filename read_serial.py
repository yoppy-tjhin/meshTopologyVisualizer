import serial, re, json
import threading
import serial.tools.list_ports

#ser = serial.Serial('COM13', 115200, timeout=0)

# while(1):
#     line = ser.readline()  # read a '\n' terminated line
#     if line:
#         #print(line.decode('utf-8'))
#         line_json = re.search(r"\s([{\[].*?[}\]])$", line.decode('utf-8'))
#         if (line_json != None):
#             print( line_json.group(1) )
#         #print('next')

serial_port = serial.Serial('COM13', 115200, timeout=0)

def handle_data(data):
    print(data)

def read_from_port(ser):
    while True:
        line = ser.readline()  # read a '\n' terminated line
        #print (line)
        if line:
            #print(line.decode('utf-8'))
            line_json = re.search(r"\s([{\[].*?[}\]])$", line.decode('utf-8'))
            if (line_json != None):
                pass
                #print( line_json.group(1) )
            print(line)

thread = threading.Thread(target=read_from_port, args=(serial_port,))
thread.start()

while True:
    pass