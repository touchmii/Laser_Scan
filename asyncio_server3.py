#!/usr/bin/env python3
"""
Pymodbus Asyncio Server Example
--------------------------------------------------------------------------

The asyncio server is implemented in pure python without any third
party libraries (unless you need to use the serial protocols which require
asyncio-pyserial). This is helpful in constrained or old environments where using
twisted is just not feasible. What follows is an example of its use:
"""
# --------------------------------------------------------------------------- #
# import the various server implementations
# --------------------------------------------------------------------------- #
import asyncio
from pymodbus.server.asyncio import StartTcpServer
from pymodbus.server.asyncio import StartUdpServer
from pymodbus.server.asyncio import StartSerialServer

from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSparseDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext

from pymodbus.transaction import ModbusRtuFramer, ModbusBinaryFramer

store = ModbusSlaveContext(
    di=ModbusSequentialDataBlock(0, [17]*100),
    co=ModbusSequentialDataBlock(0, [17]*100),
    hr=ModbusSequentialDataBlock(0, [17]*100),
    ir=ModbusSequentialDataBlock(0, [0]*100))

context = ModbusServerContext(slaves=store, single=True)
# --------------------------------------------------------------------------- #
# configure the service logging
# --------------------------------------------------------------------------- #
import logging
FORMAT = ('%(asctime)-15s %(threadName)-15s'
          ' %(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')
logging.basicConfig(format=FORMAT)
log = logging.getLogger()
log.setLevel(logging.ERROR)

# import pygame
import os
import subprocess as sp
import time
# os.environ["SDL_VIDEODRIVER"] = "dummy"

# pygame.init()
#pygame.joystick.init()

#controller = pygame.joystick.Joystick(0)
#controller.init()

# Three types of controls: axis, button, and hat
axis = {}
button = {}
hat = {}

# Assign initial data values
# Axes are initialized to 0.0
# for i in range(controller.get_numaxes()):
#     axis[i] = 0.0
# # Buttons are initialized to False
# for i in range(controller.get_numbuttons()):
#     button[i] = False
# # Hats are initialized to 0
# for i in range(controller.get_numhats()):
#     hat[i] = (0, 0)

# Labels for DS4 controller axes
AXIS_LEFT_STICK_X = 0
AXIS_LEFT_STICK_Y = 1
AXIS_RIGHT_STICK_X = 2
AXIS_RIGHT_STICK_Y = 5
AXIS_R2 = 4
AXIS_L2 = 3

# Labels for DS4 controller buttons
# Note that there are 14 buttons (0 to 13 for pygame, 1 to 14 for Windows setup)
BUTTON_SQUARE = 0
BUTTON_CROSS = 1
BUTTON_CIRCLE = 2
BUTTON_TRIANGLE = 3

BUTTON_L1 = 4
BUTTON_R1 = 5
BUTTON_L2 = 6
BUTTON_R2 = 7

BUTTON_SHARE = 8
BUTTON_OPTIONS = 9

BUTTON_LEFT_STICK = 10
BUTTON_RIGHT_STICK = 11

BUTTON_PS = 12
BUTTON_PAD = 13

# Labels for DS4 controller hats (Only one hat control)
HAT_1 = 0

X = 0
CIRCLE = 0
SQUARE = 0
TRIANGLE = 0
R2 = 0
R1 = 0
L2 = 0
L1 = 0
RIGHTSTICK_X = 0
RIGHTSTICK_Y = 0
LEFTSTICK_X = 0
LEFTSTICK_Y = 0
OPTIONS = 0
PS = 0
TRACKPAD = 0
SHARE = 0
RIGHT_ANALOG = 0
LEFT_ANALOG = 0

async def run_server(loop1):
    # ----------------------------------------------------------------------- #
    # initialize your data store
    # ----------------------------------------------------------------------- #
    # The datastores only respond to the addresses that they are initialized to
    # Therefore, if you initialize a DataBlock to addresses of 0x00 to 0xFF, a
    # request to 0x100 will respond with an invalid address exception. This is
    # because many devices exhibit this kind of behavior (but not all)::
    #
    #     block = ModbusSequentialDataBlock(0x00, [0]*0xff)
    #
    # Continuing, you can choose to use a sequential or a sparse DataBlock in
    # your data context.  The difference is that the sequential has no gaps in
    # the data while the sparse can. Once again, there are devices that exhibit
    # both forms of behavior::
    #
    #     block = ModbusSparseDataBlock({0x00: 0, 0x05: 1})
    #     block = ModbusSequentialDataBlock(0x00, [0]*5)
    #
    # Alternately, you can use the factory methods to initialize the DataBlocks
    # or simply do not pass them to have them initialized to 0x00 on the full
    # address range::
    #
    #     store = ModbusSlaveContext(di = ModbusSequentialDataBlock.create())
    #     store = ModbusSlaveContext()
    #
    # Finally, you are allowed to use the same DataBlock reference for every
    # table or you may use a separate DataBlock for each table.
    # This depends if you would like functions to be able to access and modify
    # the same data or not::
    #
    #     block = ModbusSequentialDataBlock(0x00, [0]*0xff)
    #     store = ModbusSlaveContext(di=block, co=block, hr=block, ir=block)
    #
    # The server then makes use of a server context that allows the server to
    # respond with different slave contexts for different unit ids. By default
    # it will return the same context for every unit id supplied (broadcast
    # mode).
    # However, this can be overloaded by setting the single flag to False and
    # then supplying a dictionary of unit id to context mapping::
    #
    #     slaves  = {
    #         0x01: ModbusSlaveContext(...),
    #         0x02: ModbusSlaveContext(...),
    #         0x03: ModbusSlaveContext(...),
    #     }
    #     context = ModbusServerContext(slaves=slaves, single=False)
    #
    # The slave context can also be initialized in zero_mode which means that a
    # request to address(0-7) will map to the address (0-7). The default is
    # False which is based on section 4.4 of the specification, so address(0-7)
    # will map to (1-8)::
    #
    #     store = ModbusSlaveContext(..., zero_mode=True)
    # ----------------------------------------------------------------------- #
#    store = ModbusSlaveContext(
#        di=ModbusSequentialDataBlock(0, [17]*100),
#        co=ModbusSequentialDataBlock(0, [17]*100),
#        hr=ModbusSequentialDataBlock(0, [17]*100),
#        ir=ModbusSequentialDataBlock(0, [17]*100))
#
#    context = ModbusServerContext(slaves=store, single=True)

    # ----------------------------------------------------------------------- #
    # initialize the server information
    # ----------------------------------------------------------------------- #
    # If you don't set this or any fields, they are defaulted to empty strings.
    # ----------------------------------------------------------------------- #
    identity = ModbusDeviceIdentification()
    identity.VendorName = 'Pymodbus'
    identity.ProductCode = 'PM'
    identity.VendorUrl = 'http://github.com/riptideio/pymodbus/'
    identity.ProductName = 'Pymodbus Server'
    identity.ModelName = 'Pymodbus Server'
    identity.MajorMinorRevision = '2.3.0'

    # ----------------------------------------------------------------------- #
    # run the server you want
    # ----------------------------------------------------------------------- #
    # Tcp:
    # immediately start serving:
    global context
    await StartTcpServer(context, identity=identity, address=("192.168.0.110", 2502),
                         defer_start=False, loop=loop1)
#    await joystick()

    # 	deferred start:
    # server = await StartTcpServer(context, identity=identity, address=("0.0.0.0", 5020),
    #                               allow_reuse_address=True, defer_start=True)
    #
    # asyncio.get_event_loop().call_later(20, lambda : server.serve_forever)
    # await server.serve_forever()

    # TCP with different framer
    # StartTcpServer(context, identity=identity,
    #                framer=ModbusRtuFramer, address=("0.0.0.0", 5020))

    # Udp:
    # server = await StartUdpServer(context, identity=identity, address=("0.0.0.0", 5020),
    #                               allow_reuse_address=True, defer_start=True)
    # #
    # await server.serve_forever()

    # !!! SERIAL SERVER NOT IMPLEMENTED !!!
    # Ascii:
    # StartSerialServer(context, identity=identity,
    #                    port='/dev/ttyp0', timeout=1)

    # RTU:
    # StartSerialServer(context, framer=ModbusRtuFramer, identity=identity,
    #                   port='/dev/ttyp0', timeout=.005, baudrate=9600)

    # Binary
    # StartSerialServer(context,
    #                   identity=identity,
    #                   framer=ModbusBinaryFramer,
    #                   port='/dev/ttyp0',
    #                   timeout=1)
def updating_writer(register, address, value):
#    context = context[0]
    slave_id = 0x01
    values = context[slave_id].getValues(register, address, count=5)
    values = [v + 1 for v in values]
    context[slave_id].setValues(register, address, value)

joystick_connect = 0

async def joystick():
    global joystick_connect
    updating_writer(4, 0x0, [1])
    updating_writer(4, 0x12, [1, 1])
    while True:
	#pygame.init()
        pygame.joystick.init()
        if(pygame.joystick.get_count()):
            print("connect joystick")
            joystick_connect = 1
            controller = pygame.joystick.Joystick(0)
            controller.init()
            share = 0
            # previous_time = 0
            current_time = time.time()
            print(current_time)
            while joystick_connect:
                # share_time =
                #print("tim :{}, cur_tim{}".format(time.time(), cureent_time))
                if (int(time.time() - current_time) > 250):
                    print("outtime disconnect joystick")
                    updating_writer(4, 0x0, [0])
                    joystick_connect = 0
                    stdoutdata = sp.getoutput("hcitool dc A4:15:66:DD:8A:5E")
                for event in pygame.event.get():
                    if event.type == pygame.JOYAXISMOTION:
                       # current_time = time.time()
#                        print("joyaxismotion")
                        LEFTSTICK_X = controller.get_axis(AXIS_LEFT_STICK_X)
                        LEFTSTICK_Y = controller.get_axis(AXIS_LEFT_STICK_Y)
                        RIGHTSTICK_X = controller.get_axis(AXIS_RIGHT_STICK_X)
                        RIGHTSTICK_Y = controller.get_axis(AXIS_RIGHT_STICK_Y)
                        L2 = controller.get_axis(AXIS_L2)
                        R2 = controller.get_axis(AXIS_R2)
                        a1 = int(LEFTSTICK_X/1*256)+256
                        a2 = int(LEFTSTICK_Y/1*256)+256
                        a3 = int(RIGHTSTICK_X/1*256)+256
                        a4 = int(RIGHTSTICK_Y/1*256)+256
                        a5 = int(L2/1*256)+256
                        a6 = int(R2/1*256)+256
                        updating_writer(4, 0x1, [a1, a2, a3, a4, a5, a6])
                        axis[event.axis] = round(event.value,3)
                        if (R2 > 0):
                            #print(R2)
                            current_time = time.time()
                        #print("axis :", axis[event.axis])
                    elif event.type == pygame.JOYBUTTONDOWN:
                       # current_time = time.time()
                        SQUARE = controller.get_button(0)
                        X = controller.get_button(1)
                        CIRCLE = controller.get_button(2)
                        TRIANGLE = controller.get_button(3)
                        L1 = controller.get_button(4)
                        R1 = controller.get_button(5)
                        L2 = controller.get_button(6)
                        R2 = controller.get_button(7)
                        SHARE = controller.get_button(8)
                        OPTIONS = controller.get_button(9)
                        LEFTSTICK = controller.get_button(10)
                        RIGHTSTICK = controller.get_button(11)
                        PS = controller.get_button(12)
                        TRACKPAD = controller.get_button(13)
                        button[event.button] = True
                        print('button:', button[event.button])
                        updating_writer(4, 0xa, [TRIANGLE, CIRCLE, X, SQUARE, L1, R1, L2, R2])
                        updating_writer(4, 0x7, [LEFTSTICK, RIGHTSTICK])
                        updating_writer(4, 0x14, [TRACKPAD, SHARE, OPTIONS, PS])
                        if(L1 != 0 or L2 != 0):
                            current_time = time.time()

                        #print(PS)
                        if (PS == 1):
                            #print("PS : {}".format(share))
                            share = share + 1
                            if (share == 3):
                                updating_writer(4, 0x0, [0])
                                print("manual disconnect joystick")
                                joystick_connect = 0
                                stdoutdata = sp.getoutput("hcitool dc A4:15:66:DD:8A:5E")
                    elif event.type == pygame.JOYBUTTONUP:
                        SQUARE = controller.get_button(0)
                        X = controller.get_button(1)
                        CIRCLE = controller.get_button(2)
                        TRIANGLE = controller.get_button(3)
                        L1 = controller.get_button(4)
                        R1 = controller.get_button(5)
                        L2 = controller.get_button(6)
                        R2 = controller.get_button(7)
                        SHARE = controller.get_button(8)
                        OPTIONS = controller.get_button(9)
                        LEFTSTICK = controller.get_button(10)
                        RIGHTSTICK = controller.get_button(11)
                        PS = controller.get_button(12)
                        TRACKPAD = controller.get_button(13)
                        updating_writer(4, 0xa, [TRIANGLE, CIRCLE, X, SQUARE, L1, R1, L2, R2])
                        updating_writer(4, 0x7, [LEFTSTICK, RIGHTSTICK])
                        updating_writer(4, 0x14, [TRACKPAD, SHARE, OPTIONS, PS])
                        button[event.button] = False
                    elif event.type == pygame.JOYHATMOTION:
                        #current_time = time.time()
                        hat[event.hat] = event.value
                        DPAD = controller.get_hat(0)
                        updating_writer(4, 0x12, [DPAD[0]+1,DPAD[1]+1])
                   # print(int(time.time()) - int(current_time))
                   # if (int(time.time() - current_time) > 10):
                   #     print("outtime disconnect joystick")
                   #     joystick_connect = 0
                   #     stdoutdata = sp.getoutput("hcitool dc A4:15:66:DD:8A:5E")
                await asyncio.sleep(0.005)
        pygame.joystick.quit()
        await asyncio.sleep(1)

async def detect_joystick():
    global joystick_connect
    while True:
        if(joystick_connect):
            stdoutdata = sp.getoutput("hcitool con")
            if ("A4:15:66:DD:8A:5E" not in stdoutdata.split()):
                joystick_connect = 0
                updating_writer(4, 0x0, [0])
                print("Bluetooth device is disconnected")
        await asyncio.sleep(0.5)

async def echo_angle(loop):
    reader, writer = await asyncio.open_connection('192.168.0.17', 2300,
                                                   loop=loop)

    # print('Send: %r' % message)
    # writer.write(message.encode())
    while 1:
        data = await reader.read(200)
        if(len(data) == 18):
            #data.strip()
            x = float(data[2:7])
            y = float(data[10:16])
            #print("data leng %r" % len(data))
            #print('X: {}, Y: {}'.format(x,y))
            updating_writer(4, 0x19, [int(x*100), int(y*100)])
            updating_writer(3, 0x19, [int(x*100), int(y*100)])
            #values = context[1].getValues(4, 0x19, count=2)
            #print("modbus 25 26 value: {}".format(values))
        await asyncio.sleep(0.1)

if __name__ == "__main__":
#    asyncio.run(run_server())
    loop = asyncio.get_event_loop()
    # tasks = [asyncio.Task(run_server(loop)), asyncio.Task(joystick()), asyncio.Task(detect_joystick())]
    tasks = [asyncio.Task(run_server(loop))]
    loop.run_until_complete(asyncio.wait(tasks))

