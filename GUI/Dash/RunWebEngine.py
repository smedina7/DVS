import logging
import os
import sys
import subprocess
import shlex
import sys, traceback
from PyQt5.QtCore import QThread
from PyQt5 import QtCore

class RunWebEngine(QThread):
    def __init__(self):
        logging.debug('RunWebEngine(): Instantiated')
        QThread.__init__(self)
        self.stopTriggered = False

        try:
            file_ = os.path.abspath("GUI/Dash/throughput_info.txt")
            web_engine_path = os.path.abspath("GUI/Widgets/WebEngineView.py")
            python = ''
            if sys.platform == "linux" or sys.platform == "linux2":
                python = "python3 "
            else:
                python = "python "

            self.cmd = python + web_engine_path + " " + file_
        
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            logging.error('RunWebEngine(): Error during Web Engine execution')
            traceback.print_exception(exc_type, exc_value, exc_traceback)


    def run(self):
        try:
            if sys.platform == "linux" or sys.platform == "linux2":
                logging.debug('RunWebEngine.run(): Running command: ' + str(self.cmd))
                output = subprocess.check_output(shlex.split(self.cmd))
            else: 
                output = subprocess.check_output(self.cmd)

        except Exception as e:
            if(self.stopTriggered == False):
                exc_type, exc_value, exc_traceback = sys.exc_info()
                logging.error('RunWebEngine(): Error during Web Engine execution')
                traceback.print_exception(exc_type, exc_value, exc_traceback)
            else:
                pass
            
    def stop(self):
        try:
            if sys.platform == "linux" or sys.platform == "linux2":
                python = "python3 "
                path = os.getcwd()
                os.system(python + path +"/GUI/Dash/shutdown_dash_server.py")
                print("Server Shutdown")
                self.quit()
            else:
                python = "python "
                path = os.getcwd()
                os.system(python + path +"\GUI\Dash\shutdown_dash_server.py")
                print("Server Shutdown")
                self.quit()

        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            logging.error('RunWebEngine(): Error during Web Engine termination')
            traceback.print_exception(exc_type, exc_value, exc_traceback)

    def stopTrigHandle(self):
        self.stopTriggered = True
        self.stop()
        
