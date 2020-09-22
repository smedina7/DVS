import logging
import sys

from PyQt5.QtWidgets import QApplication

from GUI.Widgets.HomeWindow import MainGUI

if __name__ == '__main__':
    if len(sys.argv) > 2:
        if os.path.exists(sys.argv[1]):
            logging.debug("MainApp(): Setting up")
        else:
            logging.debug("MainApp(): config file " + sys.argv[1] + " does not exist")

    logging.debug("MainApp(): Instantiated")

    appctxt = QApplication(sys.argv)
    gui = MainGUI()
    gui.setGeometry(500, 300, 500, 100)
    gui.show()
    exit_code = appctxt.exec_()
    sys.exit(exit_code)
    logging.debug("MainApp(): Complete")