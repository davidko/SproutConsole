#!/usr/bin/env python3

__version__ = '0.0.1'

from PyQt4 import QtCore, QtGui
import sys

try:
    from sproutconsole.mainwindow import Ui_MainWindow
except:
    from mainwindow import Ui_MainWindow

try: 
    from sproutconsole.rpi import i2c as atlasi2c
except:
    from rpi import i2c as atlasi2c

class AsyncI2c(atlasi2c.AtlasI2C):
    def __init__(self, address=99):
        super().__init__(address)
        self.poll_task = None

    def poll(self, interval, callback):
        self.poll_task = asyncio.ensure_future(self.__poll(interval, callback))

    def cancel(self):
        if self.poll_task:
            self.poll_task.cancel()
            self.poll_task = None

    @asyncio.coroutine
    def __poll(self, interval, callback):
        # Query the I2C device
        result = self.query('R')
        callback(result)
        while True:
            yield from asyncio.sleep(interval)
            result = self.query('R')
            callback(result)

class Ph(AsyncI2c):
    def __init__(self):
        super().__init__(99)

    def poll(self, interval, callback):
        def cb(res):
            callback(float(res.split()[2]))
        AsyncI2c.poll(self, interval, cb)


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
    # main()
