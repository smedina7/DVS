import logging
import subprocess
import shlex
import sys, traceback
from PyQt5.QtCore import QThread

class WiresharkRunner(QThread):
    def __init__(self, lua_scripts=None, pcap_filename=None):
        logging.debug('WiresharkRunner(): Instantiated')
        QThread.__init__(self)
        try:
            if sys.platform == "linux" or sys.platform == "linux2":

                WIRESHARK_FILENAME = "/home/kali/eceld-wireshark/wireshark-3.2.0/build/run/wireshark"
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
            exc_type, exc_value, exc_traceback = sys.exc_info()
            logging.error('WiresharkRunner(): Error during Wireshark execution')
            traceback.print_exception(exc_type, exc_value, exc_traceback)