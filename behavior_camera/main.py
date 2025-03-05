import sys
from PyQt5.QtWidgets import QApplication
from .usb_camera import USBCameraGUI


def main():
    app = QApplication(sys.argv)
    window = USBCameraGUI()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
