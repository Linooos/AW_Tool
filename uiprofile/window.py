
from PyQt5.QtWidgets import QApplication
from ui import AW_menu
import sys



def startUi():
    app = QApplication(list())

    window = AW_menu()

    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    pass
