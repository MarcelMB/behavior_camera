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
- Dual interface support:
  - Direct USB control (requires libusb)
  - OpenCV fallback for basic functionality

## System Requirements

### Required Software

- Python 3.8 or higher
- OpenCV (installed automatically)
- libusb (for direct USB camera control)

### Installing libusb

#### macOS

```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install libusb
brew install libusb
```

#### Linux (Ubuntu/Debian)

```bash
sudo apt-get update
sudo apt-get install libusb-1.0-0
```

#### Windows

1. Download the latest release from [libusb.info](https://libusb.info)
2. Extract the ZIP file
3. Copy `libusb-1.0.dll` to `C:\Windows\System32`

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
# Camera Configuration
device_id: 0  # Try device 0 first (USB camera)
resolution:
  width: 2592   # Native resolution for IMX335
  height: 1944
exposure_time: 100000  # microseconds (0.1 seconds)
gain: 5.0
auto_exposure: false
auto_gain: false

# Recording Configuration
output_directory: "recordings"
filename_format: "recording_%Y%m%d_%H%M%S.avi"
```

3. Preview the camera feed:

```bash
behavior-camera preview --config my_recording_config.yaml
```

4. Test the camera configuration:

```bash
behavior-camera test --config my_recording_config.yaml
```

5. Record video:

```bash
behavior-camera record --config my_recording_config.yaml --duration 30
```

## Camera Control Modes

The package supports two modes of camera control:

1. **Direct USB Control** (Preferred)
   - Requires libusb to be installed
   - Provides full control over camera parameters
   - Better performance and reliability
   - Used automatically when libusb is available

2. **OpenCV Fallback**
   - Used when libusb is not available
   - Basic camera functionality
   - Limited control over camera parameters
   - Works with most USB cameras

The system will automatically try direct USB control first and fall back to OpenCV if necessary.

## Development

This project uses modern Python packaging with `pyproject.toml`. To set up a development environment:

1. Clone the repository
2. Install development dependencies:

```bash
pip install -e ".[dev]"
```

## Troubleshooting

If you encounter issues:

1. **Black frames or no signal**
   - Check that the camera is properly connected
   - Try different exposure and gain settings
   - Verify the device ID in the config file

2. **USB control not working**
   - Ensure libusb is properly installed
   - Check that the camera is recognized by your system
   - Try running with elevated privileges if needed

3. **Low FPS or performance issues**
   - Check USB connection (use USB 3.0 port if available)
   - Reduce resolution if needed
   - Monitor system resource usage

4. **Permission errors**
   - On Linux, you may need to add udev rules
   - On macOS, grant camera permissions in System Preferences
   - On Windows, run as administrator if needed
