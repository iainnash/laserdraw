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
    points = []
    for idx, pointList in enumerate(pointSets):
        currentPoint = [pointList[0][0], pointList[1][0]]
        points.append(currentPoint)
        for i in range(1, len(pointList[0])):
            nextPoint = (pointList[0][i], pointList[1][i])
            # TODO(iain): Interpolate points here, at least 1000 movements?.
            points.append(nextPoint)
    
    frameLen = len(points)
    frameType = HeliosPoint * frameLen
    frame = frameType()
    for pointId in range(frameLen):
        frame[pointId] = HeliosPoint(points[pointId][0], points[pointId][1], 200, 0, 0, 200)
    return (frameLen, frame)

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

# Simple test for now
if __name__ == '__main__':
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