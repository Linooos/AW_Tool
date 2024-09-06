from siui.templates.application.application_mini_window import SiliconApplication
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

class TrayTaskWindow(SiliconApplication):
    def __init__(self):
        super().__init__()
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("./uiprofile/icon/AWCC.svg.png"))