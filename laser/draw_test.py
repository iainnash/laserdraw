# -*- coding: utf-8 -*-
"""
Example for using Helios DAC libraries in python (using C library with ctypes)
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
HeliosLib = ctypes.cdll.LoadLibrary("./libHeliosDacAPI.dylib")
numDevices = HeliosLib.OpenDevices()
print("Found ", numDevices, "Helios DACs")

#Create sample frames

def log(txt):
    print(txt)

def createFrame(pointSets, scale, offset):
    return (frameLen, frame)

class Helios:
    def __init__(self):
        self.frames = []
        # wait for laser ready
        log('Waiting for laser init')
        while HeliosLib.GetStatus(0) == 0:
            pass
        log('Has laser init')
    def addFrame(self, pointSets, scale, offset, invertX = False, invertY = False):
        points = []
        for idx, pointList in enumerate(pointSets):
            currentPoint = [int((pointList[0][0] * scale) + offset[0]), int((pointList[1][0] * scale) + offset[1])]
            points.append((currentPoint, (255, 255, 0)))
            for i in range(1, len(pointList[0])):
                nextPoint = (int((pointList[0][i] * scale) + offset[0]), int((pointList[1][i] * scale) + offset[1]))
                for i in range(2):
                    points.append((nextPoint, (255, 200, 255)))
                points.append((nextPoint, (255, 255, 0)))
        frameLen = len(points)
        frameType = HeliosPoint * frameLen
        frame = frameType()
        for pointId in range(frameLen):
            frame[pointId] = HeliosPoint(
                points[pointId][0][0],
                3000 - points[pointId][0][1],
                points[pointId][1][0],
                points[pointId][1][1],
                points[pointId][1][2],
                255
            )
        self.frames.append((frameLen, frame))
    def drawFrames(self):
        for i in range(len(self.frames)):
            statusAttempts = 0
            while (statusAttempts < 512 and HeliosLib.GetStatus(0) != 1):
                statusAttempts += 1
            HeliosLib.WriteFrame(0, 20000, 0, ctypes.pointer(self.frames[i][1]), self.frames[i][0])
            time.sleep(0.1)
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
    ], scale=3, offset=(200, 400))
    
    for i in range(0, 0xFFF - 2000, 10):
        laser.addFrame([
            [
                [65,67,72,93,115,131,142,152,164,225,233,255,255,245,210,203,195,182,172,170,161,145,101,85,38,27,27,32,48,50,0,0,5,18,38,52],
                [5,35,48,58,58,50,41,18,13,20,30,75,87,92,95,83,79,93,163,216,248,252,252,248,211,177,150,133,100,82,66,53,39,15,0,2]
            ],
        ], scale=3.0, offset=(i, 0), invertX=True)

    for i in range(100):
        laser.drawFrames()
    laser.close()
    time.sleep(1)