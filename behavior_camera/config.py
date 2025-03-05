import yaml
from typing import Dict


def load_config(config_path: str) -> Dict:
    """Load configuration from YAML file.

    Args:
        config_path: Path to configuration file

    Returns:
        Dictionary containing configuration
    """
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    # Validate configuration
    required_camera_params = [
        "framerate",
        "pixel_depth",
        "exposure_time",
        "gain",
        "auto_gain",
        "resolution",
    ]
    required_resolution_params = ["width", "height"]
    required_recording_params = ["output_directory", "file_format"]

    if "camera" not in config:
        raise ValueError("Missing 'camera' section in config")
    if "recording" not in config:
        raise ValueError("Missing 'recording' section in config")

    for param in required_camera_params:
        if param not in config["camera"]:
            raise ValueError(f"Missing required camera parameter: {param}")

    # Validate resolution parameters
    if "resolution" not in config["camera"]:
        raise ValueError("Missing resolution configuration in camera section")
    for param in required_resolution_params:
        if param not in config["camera"]["resolution"]:
            raise ValueError(f"Missing required resolution parameter: {param}")

    for param in required_recording_params:
        if param not in config["recording"]:
            raise ValueError(f"Missing required recording parameter: {param}")

    return config
