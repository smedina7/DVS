import logging
import os
import subprocess
import shlex
import sys, traceback
from PyQt5.QtCore import QThread

class RunWebEngine(QThread):
    def __init__(self, throughputfile=None):
        logging.debug('RunWebEngine(): Instantiated')
        QThread.__init__(self)
        throughput_files = os.path.join(throughputfile, "parsed/tshark")
        self.throughput_json = os.path.join(throughput_files, "networkDataXY.JSON")
        web_engine_path = os.path.abspath("GUI/Widgets/WebEngineView.py")
        python = ''
        if sys.platform == "linux" or sys.platform == "linux2":
            python = "python3 "
        else:
            python = "python "

        self.cmd = python + web_engine_path + " " + self.throughput_json

    def run(self):
        try:
            if sys.platform == "linux" or sys.platform == "linux2":
                logging.debug('RunWebEngine.run(): Running command: ' + str(self.cmd))
                output = subprocess.check_output(shlex.split(self.cmd))
            else: 
                output = subprocess.check_output(self.cmd)

        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            logging.error('RunWebEngine(): Error during Web Engine execution')
            print(e)
            traceback.print_exception(exc_type, exc_value, exc_traceback)
