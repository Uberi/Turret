# PYSERIAL IS REQUIRED TO RUN THIS PROGRAM

import serial
import serial.tools.list_ports

import sys

# obtain a list of available COM ports
try: hardware_name, description, _ = next(serial.tools.list_ports.comports())
except StopIteration:
    print("No serial ports found.")
    sys.exit(1)

print("Opening serial port " + hardware_name + ": " + description)
port = serial.Serial(hardware_name)
try:
    while True:
        command = input("Enter a command: ")
        if command == "": break
        port.write(bytes(command + "\n", "UTF-8"))
        response = str(port.readline(), "UTF-8")
        print(response, end="")
finally:
    port.close()
sys.exit(0)