#!/usr/bin/env python3

__version__ = '0.0.1'

import asyncio
from PyQt4 import QtCore, QtGui
import sys
import threading
import time

try:
    from sproutconsole.mainwindow import Ui_MainWindow
except:
    from mainwindow import Ui_MainWindow

try: 
    from sproutconsole.rpi import i2c as atlasi2c
    from sproutconsole.rpi.EC import Ec_state_machine
except:
    from rpi import i2c as atlasi2c
    from rpi.EC import Ec_state_machine 

try:
    import database
except:
    import sproutconsole.database

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

    def get(self):
        res = self.query('R')
        print(res)
        return float(res.split()[2].rstrip('\0'))

    def poll(self, interval, callback):
        def cb(res):
            res_str = res.split()[2]
            callback(float(res.split()[2].rstrip('\0')))
        AsyncI2c.poll(self, interval, cb)

class EC(AsyncI2c):
    def __init__(self, event_loop):
        super().__init__(event_loop, 100)

    def get(self):
        res = self.query('R')
        res_str = res.split()[2]
        return float( res_str.split(',')[0] )

    def poll(self, interval, callback):
        def cb(res):
            res_str = res.split()[2]
            callback( float( res_str.split(',')[0] ) )
        AsyncI2c.poll(self, interval, cb)

class StartQT4(QtGui.QMainWindow):
    def __init__(self, parent=None, asyncio_loop=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.asyncio_loop=asyncio_loop

def main():
    app = QtGui.QApplication(sys.argv)
    myapp = StartQT4()
    myapp.show()
    sys.exit(app.exec_())

class Task():
    def __init__(self, loop):
        self.loop = loop
        self.ec_log_interval = 15*60
        self.ph_log_interval = 5*60

        self.__last_ec_log_interval = 0
        self.__last_ph_log_interval = 0
        
        self.ph_device = Ph(loop)
        self.ec_device = EC(loop)

        self.ec_state_machine = Ec_state_machine()
        self.db = database.Database()

        self.running = True

    @asyncio.coroutine
    def task(self):
        while self.running:
            ph = self.ph_device.get()
            self.ph_callback(ph)
            ec = self.ec_device.get()
            self.ec_callback(ec)
            yield from asyncio.sleep(1)
        
    def ec_callback(self, ec):
        self.ec_state_machine.run(ec)
        if (time.time() - self.__last_ec_log_interval) > self.ec_log_interval:
            self.db.log('EC', float_data=ec)

    def ph_callback(self, ph):
        if (time.time() - self.__last_ph_log_interval) > self.ph_log_interval:
            self.db.log('Ph', float_data=ph)

def loop_in_thread(loop):
    asyncio.set_event_loop(loop)
    print('Running event loop...')
    task = Task(loop)
    loop.run_until_complete(task.task())
    print('Running event loop...done')

def test(loop):
    asyncio.set_event_loop(loop)
    ph = Ph(loop)
    print(ph.get())
    ec = EC(loop)
    print(ec.get())

if __name__ == '__main__':
    '''
    loop = asyncio.get_event_loop()
    t = threading.Thread(target=loop_in_thread, args=(loop,))
    t.start()    
    main()
    '''
    # test()
    loop = asyncio.get_event_loop()
    t = threading.Thread(target=test, args=(loop,))
    t.start()
    time.sleep(5)


