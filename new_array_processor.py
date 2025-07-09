import serial
import math
import time
import matplotlib.pyplot as plt
import argparse
import csv


# --- CONFIG ---

# PORT = "COM14"
BAUD = 38400
DISTANCE = 0.25  # meters
SERIAL_TIMEOUT = 0.01  # seconds
PAUSE_INTERVAL = 0.01  # seconds

# Mapping from sensor position (1–15,0) to angle
mapping = {
    1: 11.25,
    2: 33.75,
    3: 56.25,
    4: 78.75,
    5: 101.25,
    6: 123.75,
    7: 146.25,
    8: 168.75,
    9: 191.25,
    10: 213.75,
    11: 236.25,
    12: 258.75,
    13: 281.25,
    14: 303.75,
    15: 326.25,
    0: 348.75,
}


def parse_serial(line, allowed_tokens):
    """Return list of (token, position_index) for any allowed token."""
    parts = line.strip("[]\r\n ").split(",")
    out = []
    for idx, p in enumerate(parts):
        tok = p.strip()
        if len(tok) >= 3 and tok[:3] in allowed_tokens:
            out.append((tok[:3], idx + 1))
    return out


def update_plot(ax, data):
    """Clear & redraw points, with fixed axis limits."""
    ax.clear()
    for token, pos in data:
        ang = mapping.get(pos)
        if ang is None:
            continue
        phi = math.radians(90 - ang)
        x = DISTANCE * math.cos(phi)
        y = DISTANCE * math.sin(phi)
        ax.plot([0, x], [0, y], "o-")
        ax.text(x, y, f"{token} ({ang:.0f}°) ({pos})", fontsize=9)

    # lock axes to a square from –DISTANCE to +DISTANCE
    ax.set_xlim(-DISTANCE, DISTANCE)
    ax.set_ylim(-DISTANCE, DISTANCE)
    ax.set_aspect("equal", "box")

    ax.axhline(0, color="black", lw=0.5)
    ax.axvline(0, color="black", lw=0.5)
    ax.set_xlabel("X (m)")
    ax.set_ylabel("Y (m)")
    ax.set_title(f"Live 2D Plot (±{DISTANCE:.2f} m)")
    ax.grid(True)

def to_csv(data):
    """
    Takes the detected ID's and the angle its seen at at transfers them into a csv file
    """
    with open('data.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
    data_header = ['ID', 'Angle']
    writer.writerow(data_header)
    for token, pos in data:
        angle = mapping.get(pos)
        formatted_data = [token, pos]
        writer.writerow(formatted_data)
    


def main(id, port):
    try:
        ser = serial.Serial(port, BAUD, timeout=SERIAL_TIMEOUT)
        print("Serial connected")
    except Exception as e:
        print("Serial error:", e)
        return

    plt.ion()
    fig, ax = plt.subplots(figsize=(6, 6))
    allowed_tokens = {f"{id}A", f"{id}B", f"{id}C", f"{id}D"}
    # static axes setup
    ax.set_xlim(-DISTANCE, DISTANCE)
    ax.set_ylim(-DISTANCE, DISTANCE)
    ax.set_aspect("equal", "box")

    last_update = time.time()

    while True:
        raw = ser.readline().decode("utf-8", errors="ignore")
        line = raw.strip()

        if line:
            data = parse_serial(line, allowed_tokens)
            if data:
                last_update = time.time()
                angles = [mapping[p] for _, p in data if p in mapping]
                print("Angle array:", angles)
                update_plot(ax, data)

        # update the suptitle with elapsed time since last valid read
        elapsed = time.time() - last_update
        fig.suptitle(f"Last update: {elapsed:.2f} s ago")

        plt.pause(PAUSE_INTERVAL)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="IR Sensors", description="parses IR sensor information into an fov"
    )
    parser.add_argument(
        "-i", "--id", required=True, help="ID Of IR sensor you want data from"
    )
    parser.add_argument(
        "-p", "--port", required=True, help="Correct port to connect to IR sensor"
    )
    args = parser.parse_args()
    main(args.id, args.port)
