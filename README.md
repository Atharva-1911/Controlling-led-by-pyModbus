Functions used in the code:
ModbusSerialClient(): Creates a Modbus RTU client object with the given serial parameters.
connect(): Opens the serial connection to the Modbus device.
write_register(): Writes the value of led_mask to the specified Modbus holding register.
close(): Closes the Modbus serial connection.

"""
Modbus RTU LED Control using pymodbus

This script connects to a Modbus RTU slave device over a serial port
and allows the user to toggle LEDs (0–15) by writing a bitmask value
to a holding register.
"""

from pymodbus.client import ModbusSerialClient

# Modbus configuration

PORT = "COM10"          # Serial port connected to RS485/Modbus device
BAUDRATE = 9600         # Communication speed
DEVICE_ID = 1           # Modbus slave ID
REGISTER_ADDR = 0       # Holding register address to write LED states


# Create Modbus client

client = ModbusSerialClient(
    port=PORT,
    baudrate=BAUDRATE,
    parity='N',
    stopbits=1,
    bytesize=8,
    timeout=1
)
"""
ModbusSerialClient:
Creates a Modbus RTU client object configured for serial communication.
"""


# Connect to Modbus server

if not client.connect():
    """
    connect():
    Opens the serial connection to the Modbus slave.
    Returns False if connection fails.
    """
    print("Connection failed")
    exit()

print("Connected")
print("Press 0–15")
print("Type 'exit' to quit\n")


# LED state storage

led_mask = 0
"""
led_mask:
Integer used as a bitmask.
Each bit (0–15) represents the ON/OFF state of one LED.
"""


# Main loop

while True:
    user_input = input(">> ")
    """
    input():
    Reads user input from the console.
    """

    if user_input.lower() == "exit":
        break

    if user_input.isdigit():
        led = int(user_input)

        if 0 <= led <= 15:
            """
            Toggle the selected LED using XOR.
            """
            led_mask ^= (1 << led)

            client.write_register(
                address=REGISTER_ADDR,
                value=led_mask,
                device_id=DEVICE_ID
            )
            """
            write_register():
            Writes the current LED bitmask value to the Modbus holding register.
            """

            state = "ON" if (led_mask & (1 << led)) else "OFF"
            print(f"LED {led} → {state}")

        else:
            print("LED must be between 0 and 15")
    else:
        print("Invalid input")


# Close connection

client.close()
"""
close():
Closes the Modbus serial connection safely.
"""

print("Disconnected")
