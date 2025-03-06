"""
Placeholder Galaxy SDK API Interface

This module provides mock implementations of the Galaxy SDK functions
for development purposes. On Windows, this file should be replaced with
the actual SDK implementation.
"""

import numpy as np
import time


class GxPixelFormatEntry:
    MONO8 = 0x01080001
    MONO10 = 0x01100003
    MONO12 = 0x01100005
    MONO16 = 0x01100007


class gx_status_list:
    SUCCESS = 0
    ERROR = -1
    INVALID_HANDLE = -2
    INVALID_PARAMETER = -3
    NOT_FOUND_TL = -4
    NOT_FOUND_DEVICE = -5
    OFFLINE = -6
    INVALID_ACCESS = -7
    INVALID_HANDLE_INFO = -8


class DeviceManager:
    def __init__(self):
        self._devices = [GxDevice()]

    def update_all_device_list(self):
        """Update and return the list of available devices."""
        return len(self._devices), [
            {
                "vendor_name": dev.base_info.vendor_name,
                "model_name": dev.base_info.model_name,
                "sn": dev.base_info.serial_number,
                "device_class": dev.base_info.device_class,
            }
            for dev in self._devices
        ]

    def open_device_by_index(self, index):
        """Open device by index."""
        if 1 <= index <= len(self._devices):
            device = self._devices[index - 1]
            device.open()
            return device
        return None

    def open_device_by_sn(self, sn):
        """Open device by serial number."""
        for device in self._devices:
            if device.base_info.serial_number == sn:
                device.open()
                return device
        return None


class GxDeviceIPInfo:
    def __init__(self):
        self.ip = "0.0.0.0"
        self.subnet_mask = "255.255.255.0"
        self.gateway = "0.0.0.0"
        self.mac = "00:00:00:00:00:00"


class GxDeviceBaseInfo:
    def __init__(self):
        self.vendor_name = "DAHENG IMAGING"
        self.model_name = "MER-231-41U3M"
        self.serial_number = "MOCK000001"
        self.device_class = "USB3.0"
        self.ip_info = GxDeviceIPInfo()


class RemoteFeatureControl:
    def __init__(self, device):
        self._device = device

    def is_implemented(self, feature_name):
        """Check if a feature is implemented."""
        return True

    def get_float_feature(self, feature_name):
        """Get a float feature value."""
        return FloatFeature(self._device, feature_name)


class FloatFeature:
    def __init__(self, device, feature_name):
        self._device = device
        self._feature_name = feature_name

    def get(self):
        """Get the feature value."""
        return self._device.get_float_feature(self._feature_name)

    def set(self, value):
        """Set the feature value."""
        return self._device.set_float_feature(self._feature_name, value)


class GxDevice:
    def __init__(self):
        self.base_info = GxDeviceBaseInfo()
        self._is_open = False
        self._is_streaming = False
        self._exposure_time = 10000.0  # microseconds
        self._gain = 0.0
        self._width = 1920
        self._height = 1080
        self.data_stream = [GxDataStream()]
        self._remote_feature = RemoteFeatureControl(self)

    def open(self):
        if not self._is_open:
            self._is_open = True
            return gx_status_list.SUCCESS
        return gx_status_list.ERROR

    def close(self):
        if self._is_open:
            self._is_open = False
            return gx_status_list.SUCCESS
        return gx_status_list.ERROR

    def get_string_feature(self, feature_name):
        features = {
            "DeviceModelName": self.base_info.model_name,
            "DeviceVendorName": self.base_info.vendor_name,
            "DeviceSerialNumber": self.base_info.serial_number,
        }
        return features.get(feature_name, "")

    def get_float_feature(self, feature_name):
        features = {
            "ExposureTime": self._exposure_time,
            "Gain": self._gain,
        }
        return features.get(feature_name, 0.0)

    def set_float_feature(self, feature_name, value):
        if feature_name == "ExposureTime":
            self._exposure_time = value
        elif feature_name == "Gain":
            self._gain = value
        return gx_status_list.SUCCESS

    def stream_on(self):
        if not self._is_streaming:
            self._is_streaming = True
            return gx_status_list.SUCCESS
        return gx_status_list.ERROR

    def stream_off(self):
        if self._is_streaming:
            self._is_streaming = False
            return gx_status_list.SUCCESS
        return gx_status_list.ERROR

    def get_remote_device_feature_control(self):
        """Get the remote feature control interface."""
        return self._remote_feature

    def close_device(self):
        """Close the device."""
        return self.close()


class GxDataStream:
    def __init__(self):
        self._frame_count = 0

    def get_image(self):
        """Simulate getting an image from the camera."""
        self._frame_count += 1
        return GxImage()


class GxImage:
    def __init__(self):
        self._timestamp = time.time()
        self._width = 1920
        self._height = 1080
        self._pixel_format = GxPixelFormatEntry.MONO8

    def get_timestamp(self):
        return self._timestamp

    def get_width(self):
        return self._width

    def get_height(self):
        return self._height

    def get_pixel_format(self):
        return self._pixel_format

    def get_numpy_array(self):
        """Generate a mock image."""
        return np.random.randint(0, 255, (self._height, self._width), dtype=np.uint8)

    def convert(self, format_name):
        """Mock conversion."""
        return self

    def release(self):
        """Release resources."""
        pass


def gx_init():
    """Initialize the Galaxy SDK."""
    return gx_status_list.SUCCESS


def gx_device_enumerate():
    """Return a list of available devices."""
    return [GxDevice()]


def gx_device_close(handle):
    """Close a device by handle."""
    if handle and hasattr(handle, "close"):
        return handle.close()
    return gx_status_list.ERROR


def gx_deinit():
    """Deinitialize the Galaxy SDK."""
    return gx_status_list.SUCCESS
