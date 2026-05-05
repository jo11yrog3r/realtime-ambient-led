import sys
import serial
from serial.tools import list_ports

def open_serial_com(baudrate = int(115200),
                    timeout = float(1)):
    """
    Opens a serial connection to the Arduino device.

    Args:
        baudrate (int): Serial baud rate.
        timeout (float): Read timeout in seconds.

    Returns:
        serial.Serial: Open serial connection from PC -> Arduino.

    Raises:
        RuntimeError: If the port selected by the program is not found.
    """

    preferred_port = None

    if sys.platform == "win32":
        preferred_port = str("COM3")
    elif sys.platform == "linux":
        preferred_port = str("/dev/ttyACM0")

    ports = list_ports.comports()

    if not ports:
        raise RuntimeError("No serial ports found. Ensure the Arduino is plugged in.")
    
    for port in ports:
        if port.device == preferred_port:
            print(f"Successful connection to port {preferred_port}.")
            return serial.Serial(port.device, baudrate, timeout=timeout)
    raise RuntimeError(f"Program selected port {preferred_port} but it was not found. Suggest running \"python -m serial.tools.list_ports\" in terminal to list ports.")