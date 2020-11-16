import socket
# from Laser_Scan import *
from datagram_lms151 import *
# import zmqmsgbus
import numpy as np
import matplotlib.pyplot as plt
import time

TIM561_START_ANGLE = 2.3561944902  # -135° in rad
TIM561_STOP_ANGLE = -2.3561944902  # 135° in rad

fig = plt.figure()
plt.ion()

def translate(data):
    number = data['NumberOfData']
    resolution = data['AngularStepWidth']/10000
    #LMS1xx TiM5xx Start angle 0XFFF92230
    # if data['StartingAngle'] == 0xFFF92230:
    #     deg = np.arange(start=-45, stop=225, step=resolution)
    # #LMS5xx FFFF3CB0
    # elif data['StartingAngle'] == 0xFFFF3CB0:
    deg = np.arange(start=-5, stop=185, step=resolution)
    point = data['Data']
    xl = [ np.sin(np.deg2rad(deg[i-1]))*point[i-1] for i in range(number)]
    yl = [ np.cos(np.deg2rad(deg[i-1]))*point[i-1] for i in range(number)]
    # yl = [ np.cos(np.deg2rad(d))*p for p,d in point,deg]
    return xl, yl
def get_draw(s):
    s.send(b'\x02sRN LMDscandata \x03\0')

    data = s.recv(2000)
    while True:
        data = data + s.recv(2000)
        if data[-2] == 48 and data[-1] == 3 and data[-3] == 32:
            break
    datagrams_generator = decode_datagram(data)
    plt.cla()
    plt.xlim(-10, 10)
    plt.ylim(-10, 10)
    # plt.axis('off')
    return translate(datagrams_generator)

if __name__ == '__main__':
    # bus = zmqmsgbus.Bus(sub_addr='ipc://ipc/source',
    #                     pub_addr='ipc://ipc/sink')
    #
    # node = zmqmsgbus.Node(bus)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("192.168.0.30", 2112))
    # activate stream
    while True:
        s.send(b'\x02sRN LMDscandata \x03\0')

        data = s.recv(2000)
        while True:
            data = data+s.recv(2000)
            if data[-2] == 48 and data[-1] == 3 and data[-3] == 32:
                break
        datagrams_generator = decode_datagram(data)
        plt.cla()
        plt.xlim(-10, 10)
        plt.ylim(-10, 10)
        # plt.axis('off')
        xl,yl = translate(datagrams_generator)
        # plt.autoscale(False)
        # plt.axis('scaled')
        plt.plot(yl, xl)
        plt.pause(0.1)
        # plt.show()
        # time.sleep(0.5)



    # while 1:
    #     datagram = next(datagrams_generator)
    #     decoded = decode_datagram(datagram)
    #
    #     if decoded is not None:
    #         node.publish('/lidar/radius', decoded['Data'])
    #         node.publish('/lidar/theta',
    #                      np.linspace(TIM561_START_ANGLE, TIM561_STOP_ANGLE, len(decoded['Data'])).tolist())