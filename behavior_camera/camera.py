import cv2
import numpy as np
import time
from typing import Dict, Optional, Tuple
from .usb_camera import USBCamera


class Camera:
    """Camera interface for behavior recording."""

    def __init__(self, config: Dict):
        """Initialize camera interface.

        Args:
            config: Dictionary containing camera configuration
        """
        self.config = config
        self.cap = None
        self.usb_camera = None
        self.frame_count = 0
        self.last_frame_time = 0
        self.fps = 0
        self.using_usb = False  # Track which interface we're using

    def initialize(self) -> bool:
        """Initialize camera connection.

        Returns:
            bool: True if initialization successful
        """
        # First try USB direct control
        try:
            print("Attempting direct USB control...")
            self.usb_camera = USBCamera()
            if self.usb_camera.initialize():
                self.usb_camera.configure(self.config)
                print("Successfully initialized USB camera")
                self.using_usb = True
                return True
        except Exception as e:
            print(f"Direct USB control failed: {e}")
            self.usb_camera = None

        # Fall back to OpenCV if USB control fails
        try:
            print("\nFalling back to OpenCV camera control...")
            device_id = self.config.get("device_id", 0)

            # Try different backends
            backends = [
                cv2.CAP_ANY,  # Auto-detect
                cv2.CAP_AVFOUNDATION,  # macOS
                cv2.CAP_V4L2,  # Linux
                cv2.CAP_DSHOW,  # Windows
            ]

            for backend in backends:
                try:
                    print(f"\nTrying camera backend: {backend}")
                    self.cap = cv2.VideoCapture(device_id, backend)

                    if self.cap.isOpened():
                        print(f"Successfully opened camera with backend {backend}")
                        break
                except Exception as e:
                    print(f"Failed to open camera with backend {backend}: {e}")
                    continue

            if not self.cap or not self.cap.isOpened():
                print(f"Failed to open camera {device_id} with any backend")
                return False

            # Configure camera
            width = self.config["resolution"]["width"]
            height = self.config["resolution"]["height"]

            print("\nTrying to set camera properties...")

            # Try to set pixel format to MJPG for better performance
            self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))

            # Set resolution
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

            actual_width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
            actual_height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
            print(f"Requested resolution: {width}x{height}")
            print(f"Actual resolution: {actual_width}x{actual_height}")

            # Try different exposure settings
            exposure_time = self.config["exposure_time"]
            print(f"\nTrying to set exposure to {exposure_time}μs...")

            # Try both milliseconds and raw values
            exposure_attempts = [
                exposure_time / 1000.0,  # Convert to milliseconds
                exposure_time,  # Raw microseconds
                -exposure_time / 1000.0,  # Negative values sometimes work
                1.0,
                0.0,
                -1.0,  # Common fallback values
            ]

            for exp in exposure_attempts:
                print(f"Trying exposure value: {exp}")
                self.cap.set(cv2.CAP_PROP_EXPOSURE, exp)
                actual_exp = self.cap.get(cv2.CAP_PROP_EXPOSURE)
                print(f"Actual exposure: {actual_exp}")

                # Test if we're getting valid frames
                ret, frame = self.cap.read()
                if ret and frame is not None and frame.max() > 0:
                    print(f"Got valid frame with exposure {exp}")
                    break

            # Set gain
            gain = self.config["gain"]
            print(f"\nTrying to set gain to {gain}...")
            self.cap.set(cv2.CAP_PROP_GAIN, gain)
            actual_gain = self.cap.get(cv2.CAP_PROP_GAIN)
            print(f"Actual gain: {actual_gain}")

            # Handle auto exposure
            if not self.config.get("auto_exposure", True):
                print("\nTrying to disable auto exposure...")
                # Try different auto exposure modes
                for mode in [0, 1, 0.25, -1.0]:
                    print(f"Trying auto exposure mode: {mode}")
                    self.cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, mode)
                    actual_mode = self.cap.get(cv2.CAP_PROP_AUTO_EXPOSURE)
                    print(f"Actual auto exposure mode: {actual_mode}")

                    # Test if we're getting valid frames
                    ret, frame = self.cap.read()
                    if ret and frame is not None and frame.max() > 0:
                        print(f"Got valid frame with auto exposure mode {mode}")
                        break

            # Final test frames
            print("\nTesting camera output...")
            for i in range(3):
                ret, frame = self.cap.read()
                if ret and frame is not None:
                    print(f"Test frame {i + 1}:")
                    print(f"  Shape: {frame.shape}")
                    print(f"  Range: [{frame.min()}, {frame.max()}]")
                    print(f"  Mean: {frame.mean():.2f}")
                    if frame.max() <= 2:
                        print("  Warning: Frame is nearly black")
                else:
                    print(f"Failed to capture test frame {i + 1}")

            print("\nSuccessfully initialized OpenCV camera")
            self.using_usb = False
            return True

        except Exception as e:
            print(f"OpenCV initialization failed: {e}")
            return False

    def get_frame(self) -> Tuple[float, Optional[np.ndarray]]:
        """Capture a frame from the camera.

        Returns:
            Tuple of (timestamp, frame)
        """
        if self.using_usb and self.usb_camera:
            return self.usb_camera.get_frame()
        elif self.cap and self.cap.isOpened():
            timestamp = time.time()
            ret, frame = self.cap.read()

            if ret:
                self.frame_count += 1
                if self.frame_count % 30 == 0:  # Update FPS every 30 frames
                    current_time = time.time()
                    self.fps = 30 / (current_time - self.last_frame_time)
                    self.last_frame_time = current_time
                return timestamp, frame
            else:
                return timestamp, None
        else:
            return time.time(), None

    def get_fps(self) -> float:
        """Get current frames per second.

        Returns:
            float: Current FPS
        """
        return self.fps

    def release(self) -> None:
        """Release camera resources."""
        if self.usb_camera:
            self.usb_camera.release()
            self.usb_camera = None
        if self.cap:
            self.cap.release()
            self.cap = None
