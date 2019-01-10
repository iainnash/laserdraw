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
HeliosLib = ctypes.cdll.LoadLibrary("./libHeliosDacAPI.dylib")
numDevices = HeliosLib.OpenDevices()
print("Found ", numDevices, "Helios DACs")

for dev in range(numDevices):
    print('Waiting for laser init')
    while HeliosLib.GetStatus(dev) == 0:
        pass
    print('Has laser init')
    HeliosLib.Stop(dev)

HeliosLib.CloseDevices()
