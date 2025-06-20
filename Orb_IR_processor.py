import serial
import threading
import math
import matplotlib.pyplot as plt

# Mapping lists (first list of numbers and corresponding angles)
mapping_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]
mapping_angles  = [11.25, 33.75, 56.25, 78.75, 101.25, 123.75, 146.25, 168.75, 191.25, 213.75, 236.25, 258.75, 281.25, 303.75, 326.25, 348.75]

# Allowed tokens (3-letter codes)
allowed_tokens = ['72A', '72B', '72C', '72D']

def process_line(line):
    """
    Process a raw serial line (e.g. "[,27D,27D,26D:0,26D:0,,,,,27C,,,,27A,,,9c]")
    by removing the outer brackets, splitting on commas, and for each token that has
    at least three characters and whose first three characters match an allowed token,
    create an entry "Token:position" where position is comma index + 1.
    """
    if line.startswith('[') and line.endswith(']'):
        line = line[1:-1]
    tokens = line.split(',')
    allowed_data = []
    for idx, token in enumerate(tokens):
        token = token.strip()
        if len(token) >= 3:
            first_three = token[:3]
            if first_three in allowed_tokens:
                allowed_data.append(f"{first_three}:{idx+1}")
    return allowed_data

def plot_branch(distance, angle, label):
    """
    Plot a branch from (0,0) to a node at a fixed distance (in meters) and at the given angle.
    The angle is measured from the positive y-axis.
    Conversion: φ = 90° - angle, then:
       x = distance * cos(φ)
       y = distance * sin(φ)
    """
    phi = math.radians(90 - angle)
    x = distance * math.cos(phi)
    y = distance * math.sin(phi)
    plt.plot([0, x], [0, y], marker='o', label=f"{label} ({angle}°)")
    plt.text(x, y, f" {label}", fontsize=9)

def update_plot(allowed_data, distance):
    """
    Clears the plot and plots all branches from allowed_data.
    For each entry (formatted as "Token:Number"), the Number is converted to an angle
    using the mapping lists.
    """
    plt.clf()  # clear the current figure
    if allowed_data:
        print("Plotting allowed data:", allowed_data)
    else:
        print("No allowed data to plot.")
        
    for entry in allowed_data:
        try:
            token, num_str = entry.split(':')
            num = int(num_str)
            # Convert the numeric label to an angle using the mapping lists
            idx = mapping_numbers.index(num)
            angle = mapping_angles[idx]
        except Exception as e:
            print(f"Error processing entry '{entry}':", e)
            continue
        
        else:
            plot_branch(distance, angle, token)
        
    # Draw coordinate axes and labels
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    plt.xlabel("X (m)")
    plt.ylabel("Y (m)")
    plt.title("Live 2D Plot of Allowed Data (Distance = 0.25 m)")
    plt.grid(True)
    plt.xlim(-.3,.3)
    plt.ylim(-.3,.3)
    plt.legend()
    plt.draw()
    plt.pause(0.1)

def read_serial_and_plot():
    """
    Reads serial data continuously, processes each line to extract allowed data,
    converts numeric positions to angles, and updates the plot with a fixed branch length of 0.25 m.
    """
    try:
        ser = serial.Serial('COM9', baudrate=38400, timeout=1)
    except Exception as e:
        print("Could not open serial port:", e)
        return

    plt.ion()  # enable interactive mode
    plt.figure(figsize=(6, 6))
    while True:
        try:
            line_bytes = ser.readline()
            if not line_bytes:
                continue
            try:
                line_decoded = line_bytes.decode('utf-8').strip()
            except Exception as e:
                print("Decode error:", e)
                continue
            allowed_data = process_line(line_decoded)
            print("Allowed data:", allowed_data, "from line:", line_decoded)
            if allowed_data != []:
                update_plot(allowed_data, 0.25)
        except Exception as e:
            print("Error reading serial:", e)

if __name__ == '__main__':
    read_serial_and_plot()
