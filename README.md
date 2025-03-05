# Behavior Camera Control

A Python package for controlling and recording from a Sony IMX335 CMOS camera over USB interface.

## Features

- Camera control through configuration files (YAML)
- Adjustable parameters:
  - Frame rate
  - Pixel depth
  - Exposure time
  - Gain
  - Auto gain
- Video recording with timestamp synchronization
- Live preview with FPS display
- Command-line interface for easy operation

## Installation

1. Clone this repository:

```bash
git clone <repository-url>
cd behavior_camera
```

2. Create and activate a virtual environment (recommended):

```bash
# Create virtual environment
python -m venv venv

# Activate it on Mac/Linux
source venv/bin/activate
# OR on Windows
.\venv\Scripts\activate
```

3. Install the package in editable mode:

```bash
pip install -e .
```

## Usage

1. Create your configuration file:

```bash
# Copy the example config
cp config.yaml my_recording_config.yaml
```

2. Edit the configuration file (`my_recording_config.yaml`) to match your needs:

```yaml
camera:
  framerate: 30
  pixel_depth: 8
  exposure_time: 10000  # microseconds
  gain: 1.0
  auto_gain: false
  resolution:
    width: 640
    height: 480

recording:
  output_directory: "recordings"
  file_format: "avi"
```

3. Start recording:

```bash
behavior-camera record --config my_recording_config.yaml
```

4. During recording:

- A preview window will show the live camera feed with FPS
- Press Ctrl+C in the terminal to stop recording

## Development

This project uses modern Python packaging with `pyproject.toml`. To set up a development environment:

1. Clone the repository
2. Install development dependencies:

```bash
pip install -e ".[dev]"
```

## Troubleshooting

If you encounter issues:

1. Ensure your camera is properly connected and recognized by your system
2. Check that the camera resolution in config matches your camera's capabilities
3. Make sure you have write permissions in the output directory
