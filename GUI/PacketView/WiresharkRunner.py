import logging
import subprocess
import shlex
import sys, traceback
import os
from PyQt5.QtCore import QThread

class WiresharkRunner(QThread):
    def __init__(self, lua_scripts=None, pcap_filename=None):
        logging.debug('WiresharkRunner(): Instantiated')
        QThread.__init__(self)
        self.stopTriggered = False

        try:
            if sys.platform == "linux" or sys.platform == "linux2":

                WIRESHARK_FILENAME = "/usr/local/bin/wireshark"
            else:
                WIRESHARK_FILENAME = "C:\\Program Files\\Wireshark\\Wireshark.exe"

            self.cmd = WIRESHARK_FILENAME

            if pcap_filename != None:
                self.cmd += " -r " + pcap_filename
            
            if lua_scripts != None and len(lua_scripts) > 0:
                for lua_script in lua_scripts:
                    self.cmd += " -Xlua_script:" + lua_script
            
            logging.debug('WiresharkRunner(): Complete')
            
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            logging.error('WiresharkRunner(): Error during Wireshark execution')
            traceback.print_exception(exc_type, exc_value, exc_traceback)

    def run(self):
        logging.debug('WiresharkRunner.run(): Instantiated')
        try:
            if sys.platform == "linux" or sys.platform == "linux2":
                logging.debug('WiresharkRunner.run(): Running command: ' + str(self.cmd))
                output = subprocess.check_output(shlex.split(self.cmd))
            else: 
                output = subprocess.check_output(self.cmd)

            logging.debug('WiresharkRunner.run(): Complete')
            
        except Exception as e:
            if(self.stopTriggered == False):
                exc_type, exc_value, exc_traceback = sys.exc_info()
                logging.error('WiresharkRunner(): Error during Wireshark execution')
                traceback.print_exception(exc_type, exc_value, exc_traceback)
            else:
                pass

    def stop(self):
        try:
            if sys.platform == "linux" or sys.platform == "linux2":
                python = "python3 "
                path = os.getcwd()
                os.system(python + path +"/GUI/PacketView/close_wireshark.py")
                print("Quit Wireshark")
                self.quit()
            else:
                python = "python "
                path = os.getcwd()
                os.system(python + path +"\GUI\PacketView\close_wireshark.py")
                print("Quit Wireshark")
                self.quit()

        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            logging.error('RunWebEngine(): Error during Web Engine termination')
            traceback.print_exception(exc_type, exc_value, exc_traceback)

    def stopTrigHandle(self):
        self.stopTriggered = True
        self.stop()