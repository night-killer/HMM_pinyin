import sys
from input_method_slots import myMainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow


if __name__ == '__main__':

    app = QApplication(sys.argv)
    window=myMainWindow()
    window.show()
    sys.exit(app.exec_())