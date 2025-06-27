import serial
import time
#place in correct port(keep baud information)
PORT = "COM9"
BAUD = 115200

ser = serial.Serial(PORT, BAUD)

def reader(ser):
    while True: 
        read = ser.readline()
        try:
            decode = read.decode('utf-8').strip()
            print(decode)
        except:
            print("decode error")
            continue
def decoder(decode, ID):
    temp = []
    try: 
        for i in range(len(decode)):
            if 