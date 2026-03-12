import smbus
import time

bus = smbus.SMBus(1)
address = 0x48

channels = {
    "A0":0x84,
    "A1":0xC4,
    "A2":0x94,
    "A3":0xD4,
    "A4":0xB4,
    "A5":0xF4,
    "A6":0xA4,
    "A7":0xE4
}

while True:

    for name,cmd in channels.items():
        value = bus.read_byte_data(address,cmd)
        print(name,value,end="  ")

    print()
    time.sleep(1)