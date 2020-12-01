import serial
import serial.tools.list_ports
# import serial.rs485
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
    def __init__(self, port=None, baud=None):
        self.com = None
        # self.com.rs485_mode = serial.rs485.RS485Settings(rts_level_for_tx=True, rts_level_for_rx=False, loopback=False,
        #                                     delay_before_tx=None, delay_before_rx=None)
        self.x = 999
        self.y = 999
        self.query_x = bytearray.fromhex('FF 01 00 51 00 00 52')
        self.query_y = bytearray.fromhex('FF 01 00 53 00 00 54')
        self.x_0 = bytearray.fromhex('FF 01 00 4B 00 00 4C')
        self.x_90 = bytearray.fromhex('FF 01 00 4B 23 28 97')
        self.y_0 = bytearray.fromhex('FF 01 00 4D 8C A0 7A')
        self.up = bytearray.fromhex('FF 01 00 08 00 3F 48')
        self.down = bytearray.fromhex('FF 01 00 10 00 3F 50')
        self.left = bytearray.fromhex('FF 01 00 04 3F 00 44')
        self.right = bytearray.fromhex('FF 01 00 02 3F 00 42')
        self.stop = bytearray.fromhex('FF 01 00 00 00 00 01')
        self.hor = bytearray.fromhex('FF 01 00 4B 00 00 4C')
    def connect_port(self, port, baud):
        self.com = serial.Serial(port=port, baudrate=baud)
    def get_port_list(self):
        ports = serial.tools.list_ports.comports()
        return [port[0] for port in ports]
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
        time.sleep(0.2)
        # print(' '.join(map(hex, y_ret)))
        x = self.from_bytes(x_ret[-4:-2])
        y = self.from_bytes(y_ret[-4:-2])
        return x, y
    def gooPose(self, xs):
        self.com.write(self.query_x)
        x_ret = self.com.read(7)
        time.sleep(0.1)
        self.com.write(self.query_y)
        y_ret = self.com.read(7)
        time.sleep(0.2)
        # print(' '.join(map(hex, y_ret)))
        x = self.from_bytes(x_ret[-4:-2])
        y = self.from_bytes(y_ret[-4:-2])
        self.hor[-3:-1] = (xs*100).to_bytes(2, byteorder='big')
        self.hor[-1] = (0x4C + self.hor[-3] + self.hor[-2])%256
        print(self.hor)
        self.com.write(self.hor)


        return x,y
    def goPose(self, x=0, y=0):
        self.com.write(self.x_0)
        time.sleep(0.2)
        self.com.write(self.y_0)
    def goLeft(self):
        print("go left")
        self.com.write(self.left)
    def goUp(self):
        print("go up")
        self.com.write(self.up)
    def goDown(self):
        print("go down")
        self.com.write(self.down)
    def goRight(self):
        print("go right")
        self.com.write(self.right)
    def goStop(self):
        print("go stop")
        self.com.write(self.stop)


if __name__ == '__main__':
    ptz = ptz('/dev/tty.usbserial-A50285BI', 2400)
    # ptz.gooPose(90)
    # time.sleep(20)
    # ptz.gooPose(0)
    xx, yy = ptz.getPose()
    dd = int(xx / 100 + 180)
    if dd > 360:
        dd = dd - 360
    ptz.gooPose(dd)
    # for i in range(0, 180, 1):
    #     ptz.gooPose(i)
    #     time.sleep(1)
