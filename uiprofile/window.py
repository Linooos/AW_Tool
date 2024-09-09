from PyQt5.QtWidgets import QApplication
import sys
from ui import AW_menu

def startUi():
    app = QApplication(sys.argv)

    window = AW_menu()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    pass
