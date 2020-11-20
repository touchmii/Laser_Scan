import socket
# from Laser_Scan import *
from datagram_lms151 import *
# import zmqmsgbus
import numpy as np
import matplotlib.pyplot as plt
import time
import math

import cv2

from scipy.signal import savgol_filter

TIM561_START_ANGLE = 2.3561944902  # -135° in rad
TIM561_STOP_ANGLE = -2.3561944902  # 135° in rad

# fig = plt.figure()
#plt.ion()

lidar_data = b'\x02sRA LMDscandata 0 1 1160456 0 0 9506 951E 36B9861E 36B9DCCD 0 0 3F 0 0 1388 21C 1 0 0 1 DIST1 3F800000 00000000 FFFF4333 D05 23A 981 97C 982 978 97C 976 978 977 97B 97C 977 976 976 977 977 97B 978 976 977 977 97A 980 97C 980 97A 979 981 97E 98E 983 988 98A 98C 98A 945 88E 859 856 859 85B 857 85F 862 863 86A 8B3 9A7 9A5 97F 951 92D 915 909 908 913 91F 937 958 977 939 921 932 92F 909 91A 930 976 987 98D 993 997 99D 99D 9A4 9A2 9B1 9B1 9B8 9B5 9BD 9C1 999 98E 996 9A0 9B1 9D6 9E7 9AB 9CE 9EE 9E5 9F7 A07 9FB A01 A2F A3A A2C 9C8 9FF 9F4 A11 A06 9F7 A20 A39 A65 A60 A84 AA7 AA6 ABA AC3 AC8 ACD ADB ADB AD9 ADE AD2 ADF AE7 AF7 B04 B2D B57 B68 B6D B7A B90 B9B BA8 BB6 BC2 BD2 BDD BED C03 C14 C20 C2B C14 C18 C25 C3B C5A C75 C71 C81 C95 C9C C8C C77 C6A C43 C44 C37 C27 C26 942 92B 928 91C 90F 907 902 8F6 8EA 8DC 8D9 8CB 8C0 8D7 B57 B3E B28 B1E B12 B04 AFD AF6 AE2 AD9 AD1 AC7 ABA AAB AA4 A9C A8F A8B A7A A74 A66 A5E A5E A52 A4A A3B A3C A30 A2B A24 A18 A10 A07 A03 9FC 9F5 9F0 9EE 9E8 9DB 9D5 9CF 9C8 9C5 9BA 9B5 9B6 9A8 9A5 9A4 99A 992 995 993 98D 985 97D 976 975 972 972 973 963 95F 953 95E 95A 956 952 94C 942 944 941 942 936 936 935 935 933 930 928 927 927 924 91F 921 918 91B 91B 919 919 914 90F 913 90F 910 908 90D 90D 90B 907 910 908 908 908 900 908 90B 903 8F7 828 787 77F 776 774 777 779 775 777 77A 76F 76C 76F 77A 780 781 786 787 783 780 780 788 785 787 793 78C 78E 794 78D 790 790 799 797 794 7A1 79F 7A2 7A0 7A8 7AE 7B0 7AD 7A7 7AC 7B4 7BA 7C1 7CB 7C2 7CB 7CD 7D1 7D4 7DA 889 980 988 989 990 995 99A 9A0 9A2 9A6 9B1 9B8 9B8 9CA 9CB 9C6 9D7 9DF 9E3 9EA 9ED 9F0 9FD A03 A09 A0F A17 A1D A29 A33 A33 A3F A43 A47 A56 A5B A67 A70 A77 A85 A8C A95 A9F AAB AB4 AC3 AC9 AD4 AE1 AEB AF4 AFA B04 B17 B21 B31 B3D B46 B55 B63 B6A B7C B90 B94 BA3 BB2 BC2 BD5 BDD BF0 BFE C10 C24 C30 C3F C52 C63 C4D C2E C20 C04 C13 C26 C1E C1D C58 C54 C8D C96 CAC CC2 CD7 CF1 D01 D1B D24 D43 D4E D79 D90 DA7 DC2 DD3 DF7 E0F E2C E4F E69 E85 E9F EBD EDA EF8 F19 F44 100D 1059 1075 109C 10C2 10E8 111C 1163 CDF CC7 CAA C8D C6C C56 C45 C4A C4E BE9 B8A B87 B77 B78 B7B B7C B85 B97 BA8 BAC BAF BB6 1681 1686 16D5 1726 1778 17C7 1810 187C 1896 1887 1885 1878 1870 1871 1866 185D 1858 1858 184A 184C 1845 183E 1839 1839 1835 1835 1831 182C 1828 1828 1824 1822 1821 181D 1823 1855 188B 1877 1860 184A 183D 1830 181A 1815 1802 17F6 17EA 17DC 17D3 17D2 17C1 17B7 17CB 17CE 17D4 17C9 17CC 17BE 17C0 17B6 16F6 1694 1699 1697 16B7 1794 1793 1789 1781 1787 1783 1775 1774 1773 1777 1776 176E 1769 176F 176E 1767 176A 1767 1768 1768 1766 1770 1 RSSI1 3F800000 00000000 FFFF4333 D05 23A FE FE FE FD FE FE FE FE FE FE FE FE FD FC FE FC FE FE FE FE FE FE FE FE FE FE FE FE FE FD FC FD FE FE F9 CE E9 F6 F8 F8 F7 FB F9 F9 F7 FE FE FD FE FE FE FA F3 F0 F2 ED F1 F9 FC F0 C1 C5 C0 B6 AE AB B7 BB BA BB BD BB B9 BA B9 BA BB B8 B9 BA B9 AC AD AE AD B1 B2 B4 A7 BB BD AE AE B5 AA A5 BB BC BB BB BE B8 C4 BF B1 AA B9 B4 A5 B4 BD BB BA BE BA BA B8 B6 BA B3 B0 AF AD AB A9 AE B8 B9 BA BA BA BA B8 B7 B8 B5 B6 B4 B4 B5 B5 B4 A1 98 99 9A A4 A5 9E A2 AA BE C6 AE AD AC B8 C6 AF 95 CA D4 D8 D5 D5 D6 C2 CE D5 D3 D3 D2 CF E1 AD C1 CA C4 CA C9 C8 C8 C8 CA CC CC CB C9 CA CA CA CB C9 C6 CB CA CC CC CC CC CA CC C9 CB CE CD CB CC CD CD CE CD CF CE CD CF CD CC CD CF D0 D0 CE CC CF CF CE D1 D0 CE D3 D1 D0 D2 D2 D1 D0 D2 D0 CD D5 D3 D2 CF CF D0 CF D4 CF D1 D0 D4 D3 D0 D1 D0 D3 D1 D2 D3 D0 D3 D3 D3 D2 D3 D4 D3 D1 D4 D3 D6 D5 D5 D5 D7 D8 DE E3 E4 F1 FE FE FE FE FE FE FE FE FE FE FE FE FE F0 E6 E8 F7 FE FE FE FE FE FB F6 FA FA FC F0 EA F1 F2 F6 F8 FA FE FD FB FE F8 F7 FA F7 FC FD F6 F5 F8 FE F2 F6 FA F2 EB ED E9 F1 EB F6 CC CE CC CD CD CA CB CD D0 CE CF CD CF D0 CD D0 CC CF CF CC CC D0 CD CD CB CA CC C9 C8 CA CA CC C9 CA CB CB CB CA C8 CA C8 C9 C8 CB CB CA C8 C9 C9 CA C7 C8 C8 C9 C9 C9 C8 C5 C9 C7 C7 C9 CA C6 C7 C5 C6 C5 C3 C2 C4 C5 C7 C3 C6 C9 CA CC C6 B2 CE D3 B5 A9 CA AC C3 D8 D4 D0 D2 D8 D1 D0 B1 6F 57 85 C8 D4 D6 CE D2 CC C9 CB C5 D0 CF CE CD C9 CB BD AE AC B1 AE AD A9 AA 94 BD BF B7 B3 B3 BE D5 D7 D6 BB BE D2 D9 D7 D9 CD CB D7 E4 E2 E0 D8 7B 97 9A 9B 98 98 96 A2 CF D3 DD D7 D7 D9 DE D5 D7 DB D3 D4 D3 CF D4 D3 DF E1 E4 DB DD D8 DA DA DC EA E9 CA C5 C4 C3 C7 C5 C4 C5 C5 C2 C0 BF BF BE BB B5 B0 AC A9 AA B1 BA B8 B8 B8 CB D6 DD DA C8 B5 B3 B4 B0 AF B1 B1 B2 B0 B0 B2 B3 B4 B4 B5 B5 B4 B7 B8 B5 B8 BB 0 1 B SN 18220118 0 1 7B2 1 1 8 24 16 58DE0 0\x03'

def translate(data):
    number = data['NumberOfData']
    resolution = data['AngularStepWidth']/10000
#    LMS1xx TiM5xx Start angle 0XFFF92230
    if data['StartingAngle'] == 0xFFF92230:
        deg = np.arange(start=-45, stop=225, step=resolution)
     #LMS5xx FFFF3CB0
    elif data['StartingAngle'] == 0xFFFF3CB0 or data['StartingAngle'] == 0xFFFF4333:
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

def find_line(xx, yy):
    a = [[]]
    b = [[]]
    for i in range(len(xx)):
        if yy[i] > 1.7 and yy[i] < 2.1:
            if len(a[-1]) == 0:
                a[-1].append(xx[i])
                b[-1].append(yy[i])
            elif abs(yy[i] - b[-1][-1]) < 0.2 and abs(xx[i] - a[-1][-1]) < 0.2:
                a[-1].append(xx[i])
                b[-1].append(yy[i])
            elif abs(xx[i] - a[-1][-1]) > 0.3:
                a.append([xx[i]])
                b.append([yy[i]])

    return a,b
if __name__ == '__main__':
    # bus = zmqmsgbus.Bus(sub_addr='ipc://ipc/source',
    #                     pub_addr='ipc://ipc/sink')
    #
    # node = zmqmsgbus.Node(bus)

    # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # s.connect(("192.168.0.30", 2112))
    # activate stream
    #    while True:
    # s.send(b'\x02sRN LMDscandata \x03\0')

    # data = s.recv(2000)
    # while True:
    #    data = data+s.recv(2000)
    #    if data[-2] == 48 and data[-1] == 3 and data[-3] == 32:
    #        break
    datagrams_generator = decode_datagram(lidar_data)
#    plt.cla()
    plt.xlim(-10, 10)
    plt.ylim(-10, 10)
    # plt.axis('off')
    xl,yl = translate(datagrams_generator)
    # plt.autoscale(False)
    # plt.axis('scaled')
    lx, ly = find_line(yl, xl)
    xxl = savgol_filter(xl, 7, 3, mode= 'nearest')
    plt.gca().invert_yaxis()
    plt.plot(yl, xxl)
    for i in range(len(lx)-1):
        if 40 < len(ly[i]) < 100:

            plt.plot(lx[i][2:-5], ly[i][2:-5], label='ob', color='r', linewidth=1)
            # print('length: {}, X: {}, Y: {}'.format(abs(lx[i][1]-lx[i][-1]), lx[i][int(len(lx[i])/2)], ly[i][1]))
            lenth = abs(lx[i][1]-lx[i][-1])
            x_pose = lx[i][int(len(lx[i])/2)]
            y_pose = ly[i][1]
            text = 'L: {}, X: {}, Y: {}'.format(format(lenth, '.3f'), format(x_pose, '.3f'), format(y_pose, '.3f'))
            plt.text(0, 5, text, ha='center', va='bottom', fontsize=7)
#    plt.pause(0.1)
    plt.show()
    # time.sleep(0.5)



    # while 1:
    #     datagram = next(datagrams_generator)
    #     decoded = decode_datagram(datagram)
    #
    #     if decoded is not None:
    #         node.publish('/lidar/radius', decoded['Data'])
    #         node.publish('/lidar/theta',
    #                      np.linspace(TIM561_START_ANGLE, TIM561_STOP_ANGLE, len(decoded['Data'])).tolist())