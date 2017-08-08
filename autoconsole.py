#!/usr/bin/env python3

__version__ = '0.0.1'

from PyQt4 import QtCore, QtGui
import sys

try:
    from sproutconsole.mainwindow import Ui_MainWindow
except:
    from mainwindow import Ui_MainWindow

class StartQT4(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

def main():
    app = QtGui.QApplication(sys.argv)
    myapp = StartQT4()
    myapp.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
