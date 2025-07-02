import serial
import time
#place in correct port(keep baud information)
PORT = "COM9"
BAUD = 38400

ser = serial.Serial(PORT, BAUD)
#function to read the line from the serial terminal(takes data from serial terminal and decodes it into readable format)
def reader(ser):
    try:
        while True: 
            #object for reading the binary data from serial terminal
            read = ser.readline()
            #decodes binary into readble format(string format)
            decode = read.decode('utf-8').strip()
            #repeats indefinitly
            decoder(decode)
            continue
    except:
        print("decode error")
#function to parce string data into an array(ignores anything that is not a letter or number)

#start here: 
def decoder(decode):
    temp = []
   
    temp = decode.split(",")
    for i in range(len(decode)):
        if decode[i] == '[' or decode[i] == ']':
            decode.pop(i)

        print(temp)
reader(ser)