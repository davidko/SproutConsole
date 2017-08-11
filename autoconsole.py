#!/usr/bin/env python3

__version__ = '0.0.1'

import asyncio
from PyQt4 import QtCore, QtGui
import sys
import threading

try:
    from sproutconsole.mainwindow import Ui_MainWindow
except:
    from mainwindow import Ui_MainWindow

try: 
    from sproutconsole.rpi import i2c as atlasi2c
except:
    from rpi import i2c as atlasi2c

class AsyncI2c(atlasi2c.AtlasI2C):
    def __init__(self, event_loop, address=99):
        super().__init__(address)
        self.poll_task = None
        self.loop = event_loop

    def poll(self, interval, callback):
        print('Begin polling task...')
        self.poll_task = asyncio.async(self.__poll(interval, callback), loop=self.loop)
        print('Begin polling task...done')

    def cancel(self):
        if self.poll_task:
            self.poll_task.cancel()
            self.poll_task = None

    @asyncio.coroutine
    def __poll(self, interval, callback):
        print('Start polling...')
        # Query the I2C device
        result = self.query('R')
        print('Got poll result:')
        print(result)
        callback(result)
        while True:
            print('poll.')
            yield from asyncio.sleep(interval)
            result = self.query('R')
            print('Got poll result:')
            print(result)
            callback(result)

class Ph(AsyncI2c):
    def __init__(self, event_loop):
        super().__init__(event_loop, 99)

    def poll(self, interval, callback):
        def cb(res):
            res_str = res.split()[2]
            callback(float(res.split()[2].rstrip('\0')))
        AsyncI2c.poll(self, interval, cb)

class EC(AsyncI2c):
    def __init__(self, event_loop):
        super().__init__(event_loop, 100)

    def poll(self, interval, callback):
        def cb(res):
            res_str = res.split()[2]
            callback( float( res_str.split(',')[0] ) )
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

@asyncio.coroutine
def task():
    def cb(val):
        print('Poll callback!')
        print(val);
    ph = EC(loop)
    ph.poll(5, cb)
    yield from asyncio.sleep(15)
    ph.cancel()

def loop_in_thread(loop):
    asyncio.set_event_loop(loop)
    print('Running event loop...')
    loop.run_until_complete(task())
    print('Running event loop...done')

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    t = threading.Thread(target=loop_in_thread, args=(loop,))
    t.start()    


