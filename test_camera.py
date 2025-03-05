#!/usr/bin/env python3
"""
Test script for Galaxy camera interface.
This script will attempt to connect to a Galaxy camera and display its information.
"""

import sys
import time
from gxipy.gxiapi import (
    gx_init,
    gx_device_enumerate,
    gx_deinit,
    gx_status_list,
)


def print_device_info(device):
    """Print information about a Galaxy camera device."""
    print("\nDevice Information:")
    print("-" * 50)
    print(f"Vendor Name: {device.get_string_feature('DeviceVendorName')}")
    print(f"Model Name: {device.get_string_feature('DeviceModelName')}")
    print(f"Serial Number: {device.get_string_feature('DeviceSerialNumber')}")
    print(f"Device Class: {device.base_info.device_class}")
    print("-" * 50)


def print_camera_settings(device):
    """Print current camera settings."""
    print("\nCamera Settings:")
    print("-" * 50)
    print(f"Exposure Time: {device.get_float_feature('ExposureTime')} μs")
    print(f"Gain: {device.get_float_feature('Gain')} dB")
    print("-" * 50)


def main():
    """Main test function."""
    try:
        # Initialize the Galaxy SDK
        status = gx_init()
        if status != gx_status_list.SUCCESS:
            print("Failed to initialize Galaxy SDK")
            return 1

        # Find all devices
        device_list = gx_device_enumerate()
        if not device_list:
            print("No Galaxy cameras found")
            return 1

        print(f"Found {len(device_list)} Galaxy camera(s)")

        # Get the first device
        device = device_list[0]

        # Open the device
        status = device.open()
        if status != gx_status_list.SUCCESS:
            print("Failed to open camera")
            return 1

        # Print device information
        print_device_info(device)
        print_camera_settings(device)

        # Test camera streaming
        print("\nTesting camera streaming...")
        status = device.stream_on()
        if status != gx_status_list.SUCCESS:
            print("Failed to start streaming")
            return 1

        print("Camera streaming started")
        time.sleep(1)  # Wait for 1 second

        status = device.stream_off()
        if status != gx_status_list.SUCCESS:
            print("Failed to stop streaming")
            return 1

        print("Camera streaming stopped")

        # Close the device
        status = device.close()
        if status != gx_status_list.SUCCESS:
            print("Failed to close camera")
            return 1

        # Cleanup
        status = gx_deinit()
        if status != gx_status_list.SUCCESS:
            print("Failed to deinitialize Galaxy SDK")
            return 1

        print("\nTest completed successfully!")
        return 0

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
