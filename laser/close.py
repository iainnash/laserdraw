# -*- coding: utf-8 -*-
"""
Example for using Helios DAC libraries in python (using C library with ctypes)

NB: If you haven't set up udev rules you need to use sudo to run the program for it to detect the DAC.
"""
from __future__ import print_function
import ctypes
import time

#Define point structure
class HeliosPoint(ctypes.Structure):
    #_pack_=1
    _fields_ = [('x', ctypes.c_uint16),
                ('y', ctypes.c_uint16),
                ('r', ctypes.c_uint8),
                ('g', ctypes.c_uint8),
                ('b', ctypes.c_uint8),
                ('i', ctypes.c_uint8)]

#Load and initialize library
HeliosLib = ctypes.cdll.LoadLibrary("./libHeliosDacAPI.so")
numDevices = HeliosLib.OpenDevices()
print("Found ", numDevices, "Helios DACs")

#Create sample frames

def log(txt):
    print(txt)

def createFrame(pointSets):
    frameLen = sum([len(seta[0]) for seta in pointSets])
    frameType = HeliosPoint * frameLen
    frame = frameType()
    for idx, pointList in enumerate(pointSets):
        for i in range(len(pointList[0])):
            frame[i + idx * len(pointSets)] = HeliosPoint(pointList[0][i], pointList[1][i], 200, 0, 0, 200)
    return (frameLen, frame)

# #Play frames on DAC
# for i in range(300):
#     for j in range(numDevices):
#         while (HeliosLib.GetStatus(j) == 0): #Wait for ready status
#             pass
#         # Top pps = 30,000, at pps = 10,000
#         // devNum, pps, flags, points, numOfPoints
#         HeliosLib.WriteFrame(0, 10000, 0, ctypes.pointer(frames[i % 30]), 1000) #Send the frame

class Helios:
    def __init__(self):
        self.frames = []
        # wait for laser ready
        log('Waiting for laser init')
        while HeliosLib.GetStatus(0) == 0:
            pass
        log('Has laser init')
    def addFrame(self, pointSets):
        self.frames.append(createFrame(pointSets))
        print(self.frames)
    def drawFrames(self):
        for frameLen, frame in self.frames:
            HeliosLib.WriteFrame(0, 10000, 0, ctypes.pointer(frame), frameLen)
    def clearFrames(self):
        self.frames = []
    def close(self):
        HeliosLib.CloseDevices()




laser = Helios()
laser.addFrame([
    [
        [102, 102, 107, 115, 122, 154, 162, 165, 169, 229, 255, 217, 187, 168, 166, 165, 160, 90, 89, 27, 0, 35, 97],
        [0, 8, 17, 22, 23, 19, 14, 5, 6, 47, 74, 110, 99, 95, 97, 156, 202, 190, 91, 107, 54, 41, 8],
    ],
])
for i in range(100):
    laser.drawFrames()
    time.sleep(0.1)
