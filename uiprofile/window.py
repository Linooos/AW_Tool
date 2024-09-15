import os

from PyQt5.QtWidgets import QApplication


from ui import AW_menu
import sys
from SDK import globalConfig,checkGCfg
checkGCfg("globalSetting")

def startUi():
    app = QApplication(list())

    window = AW_menu()


    window.show()
    try:
        if globalConfig["globalSetting"]["minimize"]:
            window.hide()
    except KeyError:
        globalConfig["globalSetting"]["minimize"] = False
    sys.exit(app.exec_())


if __name__ == "__main__":
    pass
