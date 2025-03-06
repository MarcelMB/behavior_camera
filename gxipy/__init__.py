"""
Galaxy Camera SDK Python Interface

This package provides a Python interface for controlling Galaxy cameras.
It is designed to work with the Galaxy SDK and provides access to camera
features such as exposure control, gain settings, and image acquisition.
"""

__version__ = "2.4.2501.9211"  # Match the Galaxy SDK version

from gxipy.gxwrapper import *
from gxipy.dxwrapper import *
from gxipy.gxidef import *
from gxipy.gxiapi import *
from gxipy.DeviceManager import DeviceManager
from gxipy.Feature import Feature
from gxipy.Feature_s import Feature_s
from gxipy.FeatureControl import FeatureControl
from gxipy.Device import Device
from gxipy.DataStream import DataStream
from gxipy.ImageProcess import ImageProcess
from gxipy.ImageProcessConfig import ImageProcessConfig
from gxipy.ImageFormatConvert import ImageFormatConvert
