from pymodbus.client import ModbusSerialClient


# Modbus configuration

PORT = "COM10"          # change if needed
BAUDRATE = 9600
DEVICE_ID = 1
REGISTER_ADDR = 0

client = ModbusSerialClient(
    port=PORT,
    baudrate=BAUDRATE,
    parity='N',
    stopbits=1,
    bytesize=8,
    timeout=1
)


# Connect to Modbus server

if not client.connect():
    print("Connection failed") 
    exit()

print("Connected")
print("Press 0–15")
print("Type 'exit' to quit\n")


# LED state (bitmask)

led_mask = 0     #stores current led states as bits 

while True:
    user_input = input(">> ")

    if user_input.lower() == "exit":
        break

    if user_input.isdigit():
        led = int(user_input)

        if 0 <= led <= 15:
            # TOGGLE bit using XOR
            led_mask ^= (1 << led)

            client.write_register(
                address=REGISTER_ADDR,
                value=led_mask,
                device_id=DEVICE_ID
            )

            state = "ON" if (led_mask & (1 << led)) else "OFF"
            print(f"LED {led} → {state}")

        else:
            print("LED must be between 0 and 15")
    else:
        print("Invalid input")


client.close()
print("Disconnected")
