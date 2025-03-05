import cv2
import numpy as np
import os
import json
from typing import Dict
from datetime import datetime
import time


class VideoRecorder:
    """Video recorder with timestamp synchronization."""

    def __init__(self, output_dir: str, config: Dict):
        """Initialize video recorder.

        Args:
            output_dir: Directory to save recordings
            config: Recording configuration
        """
        self.output_dir = output_dir
        self.config = config
        self.writer = None
        self.timestamp_file = None
        self.timestamps = []

        # FPS calculation variables
        self.fps_start_time = None
        self.fps_frame_count = 0
        self.current_fps = 0
        self.fps_update_interval = 1.0  # Update FPS every second

        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

    def start_recording(self) -> None:
        """Start a new recording session."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_filename = f"recording_{timestamp}"

        # Initialize video writer
        video_path = os.path.join(self.output_dir, f"{base_filename}.avi")
        fourcc = cv2.VideoWriter_fourcc(*"XVID")

        # Get resolution from config
        width = self.config["camera"]["resolution"]["width"]
        height = self.config["camera"]["resolution"]["height"]

        self.writer = cv2.VideoWriter(
            video_path, fourcc, self.config["camera"]["framerate"], (width, height)
        )

        # Initialize timestamp file
        self.timestamp_file = open(
            os.path.join(self.output_dir, f"{base_filename}_timestamps.json"), "w"
        )
        self.timestamps = []

        # Initialize FPS calculation
        self.fps_start_time = time.time()
        self.fps_frame_count = 0
        self.current_fps = 0

    def record_frame(self, frame: np.ndarray, timestamp: float) -> None:
        """Record a frame with its timestamp and show preview.

        Args:
            frame: Video frame to record
            timestamp: UNIX timestamp of the frame
        """
        if not self.writer:
            raise RuntimeError("Recording not started")

        # Update FPS calculation
        self.fps_frame_count += 1
        elapsed_time = time.time() - self.fps_start_time

        if elapsed_time >= self.fps_update_interval:
            self.current_fps = self.fps_frame_count / elapsed_time
            self.fps_frame_count = 0
            self.fps_start_time = time.time()

        # Add FPS text to the frame
        frame_with_fps = frame.copy()
        fps_text = f"FPS: {self.current_fps:.1f}"
        cv2.putText(
            frame_with_fps,
            fps_text,
            (10, 30),  # Position: 10px from left, 30px from top
            cv2.FONT_HERSHEY_SIMPLEX,
            1,  # Font scale
            (255, 255, 255),  # Color: White
            2,  # Thickness
        )

        # Show the frame in a window
        cv2.imshow("Camera Preview", frame_with_fps)
        cv2.waitKey(1)  # Update the window, wait 1ms

        # Record the original frame (without FPS overlay)
        self.writer.write(frame)
        self.timestamps.append(timestamp)

    def stop_recording(self) -> None:
        """Stop the current recording session."""
        if self.writer:
            self.writer.release()
            self.writer = None

        if self.timestamp_file:
            json.dump({"timestamps": self.timestamps}, self.timestamp_file, indent=2)
            self.timestamp_file.close()
            self.timestamp_file = None

        # Close the preview window
        cv2.destroyAllWindows()
