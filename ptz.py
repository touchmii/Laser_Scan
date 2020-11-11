import serial
import serial.rs485
import time

# import struct
# import us

# ser = serial.Serial('com3', 9600)
# ser.rs485_mode = serial.rs485.RS485Settings(rts_level_for_tx=True, rts_level_for_rx=False, loopback=False,
#                                             delay_before_tx=None, delay_before_rx=None)
# print(ser.isOpen())
# # thestring = bytearray.fromhex('FF 01 00 04 3F 00 44')
# thestring = bytearray.fromhex('FF 01 00 51 00 00 52')
#
# print(thestring)
#
# ser.write(thestring)
# s = ser.read(7)
# print(s)
# ser.close()

class ptz():
    def __init__(self, port, baud):
        self.com = serial.Serial(port=port, baudrate=9600)
        self.com.rs485_mode = serial.rs485.RS485Settings(rts_level_for_tx=True, rts_level_for_rx=False, loopback=False,
                                            delay_before_tx=None, delay_before_rx=None)
        self.x = 999
        self.y = 999
        self.query_x = bytearray.fromhex('FF 01 00 51 00 00 52')
        self.query_y = bytearray.fromhex('FF 01 00 53 00 00 54')

    def from_bytes(self, data, big_endian=False):
        if isinstance(data, str):
            data = bytearray(data)
        if big_endian:
            data = reversed(data)
        num = 0
        for offset, byte in enumerate(data):
            num += byte << (offset * 8)
        return num
    def getPose(self):
        self.com.write(self.query_x)
        x_ret = self.com.read(7)
        time.sleep(0.1)
        self.com.write(self.query_y)
        y_ret = self.com.read(7)
        # print(' '.join(map(hex, y_ret)))
        x = self.from_bytes(x_ret[-4:-2])
        y = self.from_bytes(y_ret[-4:-2])

        return x,y
    # def gotoPose(self, x, y):

if __name__ == '__main__':
    ptz = ptz('com3', 9600)
    print(ptz.getPose())
