import sys
import os
import platform
import time
import ctypes

import bluetooth
import getch
import itertools
import operator

from ctypes import *

try:
    libEDK = cdll.LoadLibrary("C:\Users\IGORJ\Downloads\doww\community-sdk-master\examples_basic\Python\edk.dll")
except Exception as e:
    print 'Error: cannot load EDK lib:', e
    exit()

# Bluetooth setup
serverMAC = 'B8:27:EB:4F:E0:4B'
port = 1
s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
s.connect((serverMAC, port))

# Emotiv setup
IEE_EmoEngineEventCreate = libEDK.IEE_EmoEngineEventCreate
IEE_EmoEngineEventCreate.restype = c_void_p
eEvent = IEE_EmoEngineEventCreate()

IEE_EmoEngineEventGetEmoState = libEDK.IEE_EmoEngineEventGetEmoState
IEE_EmoEngineEventGetEmoState.argtypes = [c_void_p, c_void_p]
IEE_EmoEngineEventGetEmoState.restype = c_int

IEE_EmoStateCreate = libEDK.IEE_EmoStateCreate
IEE_EmoStateCreate.restype = c_void_p
eState = IEE_EmoStateCreate()

IEE_MotionDataCreate = libEDK.IEE_MotionDataCreate
IEE_MotionDataCreate.restype = c_void_p
hMotionData = IEE_MotionDataCreate();

# -------------------------------------------------------------------------

userID   = c_uint(0)
user     = pointer(userID)
state    = c_int(0)
ready    = 0
datarate = c_uint(0)
secs     = c_float(1)
motionChannelList = [i for i in range(11)]

# -------------------------------------------------------------------------

print "==================================================================="
print "Example to show how to log Motion Data from EmoDriver."
print "==================================================================="

# -------------------------------------------------------------------------

if libEDK.IEE_EngineConnect("Emotiv Systems-5") != 0:
    print "Emotiv Engine start up failed."
    
print "Start receiving IEEG Data! \n"
print "Press any key to stop logging...\n"

libEDK.IEE_MotionDataSetBufferSizeInSec(secs);
print "Buffer size in secs: %f \n" % secs.value

use_gyro = False
motion_data = 0
last_motion_data = 0
motion_center = 8192
motion_limit = 1000
motion_timer = 0
motion_timer_delay = 40

while True:
    # Getch
    char = getch.getch()
    if char == "q":
        break
    if char == "g":
        # Toggle gyro
        use_gyro = not use_gyro
    
    # Gyro
    if use_gyro:
        state = libEDK.IEE_EngineGetNextEvent(eEvent)
        if state == 0:        
            eventType = libEDK.IEE_EmoEngineEventGetType(eEvent)
            libEDK.IEE_EmoEngineEventGetUserId(eEvent, user)
            
            if eventType == 16:
                ready = 1
                print "User added"
            
            if ready == 1:
                
                libEDK.IEE_MotionDataUpdateHandle(userID, hMotionData)
                nSamplesTaken = c_uint(0)
                nSamplesTakenP = pointer(nSamplesTaken)
                
                libEDK.IEE_MotionDataGetNumberOfSample(hMotionData, nSamplesTakenP);
                
                if nSamplesTaken.value > 0:
                    dataType = c_double * nSamplesTaken.value
                    data = dataType()

                    for sampleIdx in range(nSamplesTaken.value):
                        for i in motionChannelList:
                            libEDK.IEE_MotionDataGet(hMotionData, i, data, nSamplesTaken.value)
                            if i == 1:
                                motion_data = data[sampleIdx]                                           
        elif state != 0x0600:
            print "Internal error in Emotiv Engine ! "
            motion_data = motion_center

    # Send data over bluetooth
    send_data = "z"

    if use_gyro:
        if motion_timer > 0:
            if char == "w" or char == "s":
                send_data = char
            else:
                send_data = "z"
        else:
            if char == "a" or char == "d" or char == "z":
                # left -> pos
                # right -> neg

                if motion_data - motion_center > motion_limit:
                    send_data = "a"
                    motion_timer = motion_timer_delay
                elif motion_data - motion_center < -motion_limit:
                    send_data = "d"
                    motion_timer = motion_timer_delay
                else:
                    send_data = "z"

            else:
                send_data = char

        motion_timer -= 1
    else:
        send_data = char

    s.send(send_data)

    print char, '--', motion_data, use_gyro, "SENT: ", send_data
    last_motion_data = motion_data

while True:
    print GetAccelData()


# -------------------------------------------------------------------------

s.close()

libEDK.IEE_EngineDisconnect()
libEDK.IEE_EmoStateFree(eState)
libEDK.IEE_EmoEngineEventFree(eEvent)
