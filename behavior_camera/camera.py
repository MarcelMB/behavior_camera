import cv2
import numpy as np
import time
from typing import Dict, Optional, Tuple


class Camera:
    """Camera interface for Sony IMX335 CMOS sensor."""

    def __init__(self, device_id: int = 0):
        """Initialize camera interface.

        Args:
            device_id: Camera device ID (default: 0)
        """
        self.device_id = device_id
        self.cap = None
        self.current_config = {}

    def initialize(self) -> bool:
        """Initialize camera connection."""
        # For macOS, we use the AVFoundation backend
        self.cap = cv2.VideoCapture(self.device_id, cv2.CAP_AVFOUNDATION)

        if not self.cap.isOpened():
            print(f"Failed to open camera device {self.device_id}")
            return False

        # Print camera properties for debugging
        print("\nCamera opened successfully:")
        print(f"Backend: {self.cap.getBackendName()}")

        # Try setting some initial values to get an image
        self.cap.set(
            cv2.CAP_PROP_AUTO_EXPOSURE, 0.75
        )  # Different value for auto exposure
        self.cap.set(cv2.CAP_PROP_BRIGHTNESS, 0.5)  # Mid brightness
        time.sleep(1)  # Give camera time to adjust

        # Get all camera properties
        props = [
            ("Width", cv2.CAP_PROP_FRAME_WIDTH),
            ("Height", cv2.CAP_PROP_FRAME_HEIGHT),
            ("FPS", cv2.CAP_PROP_FPS),
            ("Format", cv2.CAP_PROP_FORMAT),
            ("Mode", cv2.CAP_PROP_MODE),
            ("Brightness", cv2.CAP_PROP_BRIGHTNESS),
            ("Contrast", cv2.CAP_PROP_CONTRAST),
            ("Saturation", cv2.CAP_PROP_SATURATION),
            ("Exposure", cv2.CAP_PROP_EXPOSURE),
            ("Auto Exposure", cv2.CAP_PROP_AUTO_EXPOSURE),
            ("Gain", cv2.CAP_PROP_GAIN),
        ]

        print("\nInitial camera properties:")
        for prop_name, prop_id in props:
            value = self.cap.get(prop_id)
            print(f"{prop_name}: {value}")

        # Try to grab a test frame
        ret, frame = self.cap.read()
        if ret:
            print(
                f"\nTest frame captured successfully. Shape: {frame.shape}, dtype: {frame.dtype}"
            )
            if np.all(frame == 0):
                print("Warning: Test frame is completely black")
            else:
                print(
                    f"Frame statistics - Min: {frame.min()}, Max: {frame.max()}, Mean: {frame.mean():.2f}"
                )
        else:
            print("Failed to capture test frame")

        return True

    def configure(self, config: Dict) -> None:
        """Configure camera parameters.

        Args:
            config: Dictionary containing camera configuration
        """
        if not self.cap:
            raise RuntimeError("Camera not initialized")

        print("\nConfiguring camera...")

        # Set resolution first
        width = config["resolution"]["width"]
        height = config["resolution"]["height"]
        print(f"Setting resolution to {width}x{height}")
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

        # Set frame rate
        print(f"Setting framerate to {config['framerate']}")
        self.cap.set(cv2.CAP_PROP_FPS, config["framerate"])

        # Try different auto exposure values
        if config["auto_gain"]:
            print("Trying different auto exposure settings...")
            for auto_exp in [0.75, 1, 2, 3]:  # Try different values
                print(f"Testing auto exposure value: {auto_exp}")
                self.cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, auto_exp)
                time.sleep(0.5)

                # Check if we get a non-black frame
                ret, frame = self.cap.read()
                if ret and not np.all(frame == 0):
                    print(f"Found working auto exposure value: {auto_exp}")
                    break

            # Set some initial brightness and contrast
            self.cap.set(cv2.CAP_PROP_BRIGHTNESS, 0.5)
            self.cap.set(cv2.CAP_PROP_CONTRAST, 0.5)
        else:
            # Manual exposure settings
            print("Setting manual exposure...")
            self.cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0)
            exposure_ms = config["exposure_time"] / 1000
            print(f"Setting exposure to {exposure_ms}ms")
            self.cap.set(cv2.CAP_PROP_EXPOSURE, exposure_ms)
            self.cap.set(cv2.CAP_PROP_GAIN, config["gain"])

        # Verify final settings
        print("\nFinal camera configuration:")
        props = [
            ("Width", cv2.CAP_PROP_FRAME_WIDTH),
            ("Height", cv2.CAP_PROP_FRAME_HEIGHT),
            ("FPS", cv2.CAP_PROP_FPS),
            ("Brightness", cv2.CAP_PROP_BRIGHTNESS),
            ("Contrast", cv2.CAP_PROP_CONTRAST),
            ("Exposure", cv2.CAP_PROP_EXPOSURE),
            ("Auto Exposure", cv2.CAP_PROP_AUTO_EXPOSURE),
            ("Gain", cv2.CAP_PROP_GAIN),
        ]

        for prop_name, prop_id in props:
            value = self.cap.get(prop_id)
            print(f"{prop_name}: {value}")

        self.current_config = config

    def get_frame(self) -> Tuple[float, Optional[np.ndarray]]:
        """Capture a frame from the camera.

        Returns:
            Tuple of (timestamp, frame)
        """
        if not self.cap:
            raise RuntimeError("Camera not initialized")

        # Try to read a few frames if the first one fails
        max_attempts = 3
        for attempt in range(max_attempts):
            timestamp = time.time()
            ret, frame = self.cap.read()

            if ret and frame is not None:
                if np.all(frame == 0):
                    print(f"Warning: Frame {attempt + 1} is completely black")
                    if attempt < max_attempts - 1:
                        time.sleep(0.1)
                        continue
                return timestamp, frame

            if attempt < max_attempts - 1:
                print(f"Frame capture attempt {attempt + 1} failed, retrying...")
                time.sleep(0.1)

        print("Failed to capture valid frame")
        return timestamp, None

    def release(self) -> None:
        """Release camera resources."""
        if self.cap:
            self.cap.release()
            self.cap = None
