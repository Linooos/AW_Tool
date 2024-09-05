from PyQt5.QtWidgets import QApplication
import sys
from ui import AW_menu

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = AW_menu()
    window.show()

    sys.exit(app.exec_())
