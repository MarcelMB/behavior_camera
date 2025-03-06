"""
Galaxy Camera SDK Python Interface

This package provides a Python interface for controlling Galaxy cameras.
It is designed to work with the Galaxy SDK and provides access to camera
features such as exposure control, gain settings, and image acquisition.
"""

__version__ = "2.4.2501.9211"  # Match the Galaxy SDK version

from .gxiapi import (
    DeviceManager,
    GxDevice,
    GxPixelFormatEntry,
    gx_status_list,
    gx_init,
    gx_device_enumerate,
    gx_device_close,
    gx_deinit,
)
