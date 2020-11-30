import socket
# from Laser_Scan import *
from datagram_lms151 import *
# import zmqmsgbus
import numpy as np
import matplotlib.pyplot as plt
import time

TIM561_START_ANGLE = 2.3561944902  # -135° in rad
TIM561_STOP_ANGLE = -2.3561944902  # 135° in rad


# plt.ion()

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

def read_file(name):
    f = open(name,'r')
    lidar_datas = bytes(f.read(), encoding='utf-8')
    data_list = lidar_datas.split(b'\x03\n')
    data_list.remove(data_list[-1])
    data_list.remove(data_list[-1])
    p = []
    for i in data_list:
        p.append(decode_datagram(i))
    return p

def translate3d(d):
    deg_phi = np.arange(start=-5, stop=185, step=0.3333)
    deg_phi2 = np.arange(start=185, stop=-5, step=-0.3333)
    deg_theta = np.arange(start=0, stop=180, step=180/len(d))
    deg_theta2 = np.arange(start=180, stop=360, step=180/len(d))
    # deg_theta = np.arange(start=180, stop=0, step=-180/884)
    # deg_theta2 = np.arange(start=360, stop=180, step=-180/884)
    x, y, z = [], [], []
    for p in range(len(d)):
    # for p in range(0, 1, 1):
        p_number = d[p]['NumberOfData']
        point = d[p]['Data']
        # z.extend( [ np.cos(np.deg2rad(deg_phi[i-1]))*point[i-1] for i in range(p_number)] )
        # x.extend( [ np.sin(np.deg2rad(deg_phi[i-1]))*np.cos(np.deg2rad(deg_theta[i-1]))*point[i-1] for i in range(285)] )
        # x.extend( [ np.sin(np.deg2rad(deg_phi[i-1]))*np.cos(np.deg2rad(deg_theta2[i-1]))*point[i-1] for i in range(285, p_number, 1)] )
        # y.extend( [ np.sin(np.deg2rad(deg_phi[i-1]))*np.sin(np.deg2rad(deg_theta[i-1]))*point[i-1] for i in range(285)] )
        # y.extend( [ np.sin(np.deg2rad(deg_phi[i-1]))*np.sin(np.deg2rad(deg_theta2[i-1]))*point[i-1] for i in range(285, p_number, 1)] )
        z.extend( [ np.sin(np.deg2rad(deg_phi2[i]))*point[i] for i in range(570)] )
        # z.extend( [ np.sin(np.deg2rad(deg_phi2[i+285]))*point[-i-1] for i in range(285)] )
        x.extend( [ np.cos(np.deg2rad(deg_phi[i]))*np.cos(np.deg2rad(deg_theta[p]))*point[i] for i in range(285)] )
        x.extend( [ np.cos(np.deg2rad(deg_phi[i+284]))*np.cos(np.deg2rad(deg_theta[p]))*(point[i+285]) for i in range(285)] )
        y.extend( [ np.cos(np.deg2rad(deg_phi[i]))*np.sin(np.deg2rad(deg_theta[p]))*point[i] for i in range(285)] )
        y.extend( [ np.cos(np.deg2rad(deg_phi[i+284]))*np.sin(np.deg2rad(deg_theta[p]))*(point[i+285]) for i in range(285)] )


    return x, y, z

def create_output(vertices, colors, filename):
    colors = colors.reshape(-1, 3)
    vertices = np.hstack([vertices.reshape(-1, 3), colors])
    np.savetxt(filename, vertices, fmt='%f %f %f %d %d %d')     # 必须先写入，然后利用write()在头部插入ply header
    ply_header = '''ply\nformat ascii 1.0\nelement vertex %(vert_num)d\nproperty float x\nproperty float y\nproperty float z\nproperty uchar red\nproperty uchar green\nproperty uchar blue\nend_header\n'''
    with open(filename, 'r+') as f:
        old = f.read()
        f.seek(0)
        f.write(ply_header % dict(vert_num=len(vertices)))
        f.write(old)

if __name__ == '__main__':
    # bus = zmqmsgbus.Bus(sub_addr='ipc://ipc/source',
    #                     pub_addr='ipc://ipc/sink')
    #
    # node = zmqmsgbus.Node(bus)
    fig = plt.figure()
    x, y, z = translate3d(read_file('data2020-11-29-09-15.txt'))
    a = []
    for i in range(len(x)-1):
        a.append([x[i], y[i], z[i]])
    aa = np.array(a)

    b = np.float32(aa)
    #   43867是我的点云的数量，用的时候记得改成自己的
    one = np.ones((len(x)-1, 3))
    one = np.float32(one) * 255
    #    points_3D = np.array([[1,2,3],[3,4,5]]) # 得到的3D点（x，y，z），即2个空间点
    #    colors = np.array([[0, 255, 255], [0, 255, 255]])   #给每个点添加rgb
    # Generate point cloud
    print("\n Creating the output file... \n")
    #    create_output(points_3D, colors, output_file)
    output_file = 'Andre_Agassi_0019.ply'
    create_output(b, one, output_file)
    ax = plt.axes(projection='3d')
    ax.scatter3D(x, y, z)
    # ax.contour3D(x, y, z, 50, cmap='binary')
    # ax.set_xlabel('x')
    # ax.set_ylabel('y')
    # ax.set_zlabel('z')
    ax.view_init(60, 35)
    plt.show()
    # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # s.connect(("192.168.0.30", 2112))
    # # activate stream
    # while True:
    #     s.send(b'\x02sRN LMDscandata \x03\0')
    #
    #     data = s.recv(2000)
    #     while True:
    #         data = data+s.recv(2000)
    #         if data[-2] == 48 and data[-1] == 3 and data[-3] == 32:
    #             break
    #     datagrams_generator = decode_datagram(data)
    #     plt.cla()
    #     plt.xlim(-10, 10)
    #     plt.ylim(-10, 10)
    #     # plt.axis('off')
    #     xl,yl = translate(datagrams_generator)
    #     # plt.autoscale(False)
    #     # plt.axis('scaled')
    #     plt.plot(yl, xl)
    #     plt.pause(0.1)
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