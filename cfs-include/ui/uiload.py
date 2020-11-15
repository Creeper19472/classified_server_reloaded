import sys
from PyQt5.QtWidgets import QApplication, QWizard
from ui1 import *


class MyWindow(QWizard, Ui_Wizard):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = MyWindow()
    myWin.show()
    sys.exit(app.exec_())
