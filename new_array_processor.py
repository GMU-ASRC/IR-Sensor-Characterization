import serial
import time
import argparse

# Mapping lists (first list of numbers and corresponding angles)
mapping_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]
mapping_angles  = [11.25, 33.75, 56.25, 78.75, 101.25, 123.75, 146.25, 168.75, 191.25, 213.75, 236.25, 258.75, 281.25, 303.75, 326.25, 348.75]

def reader(ser):
    while True: 
        read = ser.readline()
        try:
            decode = read.decode('utf-8').strip()
            print(decode)
        except:
            print("decode error")
            continue
def decoder(decode, id):
    temp = []
    try: 
        temp = decode.split(",")
        print(temp)
    except:
        
def main(id, port):
    id_string = str(id)
    allowed_data = [f"{id_string}A", f"{id_string}B", f"{id_string}C", f"{id_string}D"] 
    try:
        serial = serial.Serial(38400, port) #38400 should be the correct baudrate
    except:
        print("serial error, port or baudrate")

    

if __name__ == '__main__':
    print("")
    parser = argparse.ArgumentParser(
            prog='IR Sensors',
            description='parses IR sensor information into an fov'
    )
    parser.add_argument('-i', "--id", required=True, help="ID Of IR sensor you want data from")
    parser.add_argument('-p', "--port",  required=True, help="Correct port to connect to IR sensor")
    args = parser.parse_args()    
    main(args.id,args.port)
    