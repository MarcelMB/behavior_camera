import gxipy as gx
import cv2
from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QSpinBox,
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap


class USBCameraGUI(QMainWindow):
    """Simple GUI for camera control using Galaxy SDK."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Camera Control")
        self.setGeometry(100, 100, 800, 600)

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Create image display
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.image_label)

        # Create control panel
        control_layout = QHBoxLayout()

        # Exposure control
        exposure_layout = QVBoxLayout()
        exposure_layout.addWidget(QLabel("Exposure (μs):"))
        self.exposure_spinbox = QSpinBox()
        self.exposure_spinbox.setRange(1, 1000000)
        self.exposure_spinbox.setValue(10000)
        self.exposure_spinbox.valueChanged.connect(self.set_exposure)
        exposure_layout.addWidget(self.exposure_spinbox)
        control_layout.addLayout(exposure_layout)

        # Gain control
        gain_layout = QVBoxLayout()
        gain_layout.addWidget(QLabel("Gain:"))
        self.gain_spinbox = QSpinBox()
        self.gain_spinbox.setRange(0, 24)
        self.gain_spinbox.setValue(0)
        self.gain_spinbox.valueChanged.connect(self.set_gain)
        gain_layout.addWidget(self.gain_spinbox)
        control_layout.addLayout(gain_layout)

        # Control buttons
        button_layout = QVBoxLayout()
        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.start_capture)
        button_layout.addWidget(self.start_button)

        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.stop_capture)
        self.stop_button.setEnabled(False)
        button_layout.addWidget(self.stop_button)

        control_layout.addLayout(button_layout)
        layout.addLayout(control_layout)

        # Initialize camera
        self.camera = USBCamera()

        # Setup timer for frame updates
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

        # Initialize state
        self.is_capturing = False

    def set_exposure(self, value):
        """Set camera exposure time."""
        if self.camera.is_initialized:
            self.camera.set_exposure(value)

    def set_gain(self, value):
        """Set camera gain."""
        if self.camera.is_initialized:
            self.camera.set_gain(value)

    def start_capture(self):
        """Start camera capture."""
        if not self.is_capturing:
            if self.camera.start_capture():
                self.is_capturing = True
                self.timer.start(33)  # ~30 FPS
                self.start_button.setEnabled(False)
                self.stop_button.setEnabled(True)

    def stop_capture(self):
        """Stop camera capture."""
        if self.is_capturing:
            self.camera.stop_capture()
            self.is_capturing = False
            self.timer.stop()
            self.start_button.setEnabled(True)
            self.stop_button.setEnabled(False)

    def update_frame(self):
        """Update the displayed frame."""
        timestamp, frame = self.camera.get_frame()
        if frame is not None:
            # Convert frame to RGB format
            if len(frame.shape) == 2:  # Mono
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
            else:  # Already RGB
                rgb_frame = frame

            height, width, channels = rgb_frame.shape
            bytes_per_line = channels * width

            # Convert to QImage and display
            qt_image = QImage(
                rgb_frame.data, width, height, bytes_per_line, QImage.Format_RGB888
            )
            pixmap = QPixmap.fromImage(qt_image)

            # Scale to fit label while maintaining aspect ratio
            scaled_pixmap = pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio)
            self.image_label.setPixmap(scaled_pixmap)

    def closeEvent(self, event):
        """Handle window close event."""
        self.stop_capture()
        self.camera.release()
        event.accept()


class USBCamera:
    """Galaxy SDK camera interface."""

    def __init__(self):
        """Initialize camera interface."""
        self.device_manager = None
        self.cam = None
        self.is_initialized = False
        self.initialize()

    def initialize(self) -> bool:
        """Initialize camera connection."""
        try:
            # Create device manager
            self.device_manager = gx.DeviceManager()

            # Get device list
            dev_num, dev_info_list = self.device_manager.update_all_device_list()
            if dev_num == 0:
                print("No devices found")
                return False

            # Open first available device
            self.cam = self.device_manager.open_device_by_sn(dev_info_list[0].get("sn"))

            # Get remote device feature control
            self.remote_device = self.cam.get_remote_device_feature_control()

            # Set default parameters
            if self.remote_device.is_implemented("ExposureTime"):
                self.remote_device.get_float_feature("ExposureTime").set(
                    10000
                )  # 10ms default exposure

            if self.remote_device.is_implemented("Gain"):
                self.remote_device.get_float_feature("Gain").set(0)  # 0dB default gain

            self.is_initialized = True
            print("Camera initialized successfully")
            return True

        except Exception as e:
            print(f"Initialization error: {str(e)}")
            self.is_initialized = False
            return False

    def set_exposure(self, exposure_time: float) -> None:
        """Set exposure time in microseconds."""
        try:
            if self.is_initialized and self.remote_device.is_implemented(
                "ExposureTime"
            ):
                self.remote_device.get_float_feature("ExposureTime").set(exposure_time)
        except Exception as e:
            print(f"Error setting exposure: {str(e)}")

    def set_gain(self, gain: float) -> None:
        """Set gain in dB."""
        try:
            if self.is_initialized and self.remote_device.is_implemented("Gain"):
                self.remote_device.get_float_feature("Gain").set(gain)
        except Exception as e:
            print(f"Error setting gain: {str(e)}")

    def start_capture(self) -> bool:
        """Start image capture."""
        try:
            if self.is_initialized:
                self.cam.stream_on()
                return True
        except Exception as e:
            print(f"Error starting capture: {str(e)}")
        return False

    def stop_capture(self) -> None:
        """Stop image capture."""
        try:
            if self.is_initialized:
                self.cam.stream_off()
        except Exception as e:
            print(f"Error stopping capture: {str(e)}")

    def get_frame(self):
        """Get a frame from the camera."""
        try:
            if not self.is_initialized:
                return None, None

            # Get raw frame
            raw_image = self.cam.data_stream[0].get_image()
            if raw_image is None:
                return None, None

            timestamp = raw_image.get_timestamp()

            # Convert to numpy array
            if raw_image.get_pixel_format() == gx.GxPixelFormatEntry.MONO8:
                frame = raw_image.get_numpy_array()
            else:
                # Convert to RGB if needed
                frame = raw_image.convert("RGB")
                if frame is not None:
                    frame = frame.get_numpy_array()

            raw_image.release()  # Release the raw image
            return timestamp, frame

        except Exception as e:
            print(f"Error getting frame: {str(e)}")
            return None, None

    def release(self) -> None:
        """Release camera resources."""
        try:
            if self.cam:
                self.stop_capture()
                self.cam.close_device()
            self.is_initialized = False
        except Exception as e:
            print(f"Error releasing camera: {str(e)}")
