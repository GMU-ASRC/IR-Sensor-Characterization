import serial

#place in correct port(keep baud information)
PORT = "COM10"
BAUD = 115200

ser = serial.Serial(PORT, BAUD)

def array_processor(ID):
    