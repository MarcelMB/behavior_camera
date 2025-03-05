# Windows Setup Guide for Galaxy Camera Interface

## Prerequisites

1. Install Python 3.11 or later
2. Install Galaxy SDK from Daheng Imaging website
3. Visual Studio Code (recommended)

## Installation Steps

1. **Install Galaxy SDK**
   - Download "Galaxy Windows SDK (V2)" from https://www.galaxyview.com/en/Download/
   - Run the installer
   - Make note of the installation directory (default: `C:\Program Files\Daheng Imaging\GalaxySDK`)

2. **Set Up Python Environment**
   ```cmd
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   venv\Scripts\activate
   
   # Install required packages
   pip install -e .
   pip install PyQt5 opencv-python numpy pillow
   ```

3. **Copy SDK Files**
   ```cmd
   # Create gxipy directory
   mkdir gxipy
   
   # Copy SDK Python files
   xcopy /E /I "C:\Program Files\Daheng Imaging\GalaxySDK\Development\Samples\Python\gxipy" "gxipy"
   ```

4. **Add SDK DLLs to PATH**
   - Add `C:\Program Files\Daheng Imaging\GalaxySDK\Bin\Win64` to your system PATH
   - Or run this command as administrator:
     ```cmd
     setx PATH "%PATH%;C:\Program Files\Daheng Imaging\GalaxySDK\Bin\Win64"
     ```

## Testing the Camera

1. Connect your Galaxy camera to USB
2. Run the test script:
   ```cmd
   python test_camera.py
   ```

The test script will:
- List all connected cameras
- Try to open the first camera
- Display current settings
- Capture a test frame
- Save the frame as 'test_frame.png'

## Troubleshooting

1. **ModuleNotFoundError: No module named 'gxipy'**
   - Make sure you've copied the SDK files correctly
   - Verify the gxipy directory is in your project root

2. **DLL Load Failed**
   - Make sure the SDK Bin directory is in your system PATH
   - Try restarting your terminal/VS Code

3. **Permission Errors**
   - Try running as administrator
   - Check USB permissions in Device Manager

4. **Camera Not Found**
   - Verify camera is connected and powered
   - Check Device Manager for proper driver installation
   - Try a different USB port (preferably USB 3.0) 