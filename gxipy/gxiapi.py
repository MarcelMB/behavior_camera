"""
Placeholder Galaxy SDK API Interface

This module provides mock implementations of the Galaxy SDK functions
for development purposes. On Windows, this file should be replaced with
the actual SDK implementation.
"""


class gx_status_list:
    SUCCESS = 0
    ERROR = -1


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


class GxDevice:
    def __init__(self):
        self.base_info = GxDeviceBaseInfo()
        self._is_open = False
        self._is_streaming = False
        self._exposure_time = 10000.0  # microseconds
        self._gain = 0.0
        self._width = 1920
        self._height = 1080

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
