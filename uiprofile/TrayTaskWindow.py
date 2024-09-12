
from PyQt5.QtWidgets import QApplication, QMainWindow, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QObject, QEvent
from uiprofile.miniApp import miniApp
from SDK import saveConfig
class TrayTaskWindow(miniApp):
    windowState = True
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("./uiprofile/icon/AWCC.svg.png"))

        show_action = QAction("显示", self)
        show_action.triggered.connect(self.show_window)
        quit_action = QAction("退出", self)
        quit_action.triggered.connect(QApplication.instance().quit)

        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(quit_action)

        self.tray_icon.setContextMenu(tray_menu)

        self.tray_icon.activated.connect(self.on_tray_icon_activated)
        self.tray_icon.show()

        self.installEventFilter(self)

    def closeEvent(self, event):
        saveConfig()


    def show_window(self):
        self.window().show()
        self.layerMain().show()
        self.activateWindow()

    def on_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.show_window()
            self.windowState = True
        if reason == QSystemTrayIcon.Trigger:
            self.window().hide()
            self.windowState = False

    # def eventFilter(self, source, event):
    #     if event.type() == QEvent.WindowDeactivate:
    #         #self.window().hide()
    #         self.windowState = False
    #     return super().eventFilter(source, event)