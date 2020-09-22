import logging
import sys
from GUI.Widgets.HomeWindow import MainGUI
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5.uic import loadUi


class DVSstartUpPage(QMainWindow):
    def __init__(self):
        super(DVSstartUpPage, self).__init__()
        loadUi('GUI/src/DVSstartUpPage.ui', self)

        self.CreateNew_pushButton = self.findChild(QPushButton, 'CreateNew_pushButton')
        self.CreateNew_pushButton.clicked.connect(self.openMain)

        self.show()

    def openMain(self):
        self.window = MainGUI()
        self.window.setGeometry(500, 300, 500, 100)
        self.window.show()
        self.close()
        
if __name__ == "__main__":
    if len(sys.argv) > 2:
        if os.path.exists(sys.argv[1]):
            logging.debug("MainApp(): Setting up")
        else:
            logging.debug("MainApp(): config file " + sys.argv[1] + " does not exist")

    logging.debug("MainApp(): Instantiated")


    app = QApplication(sys.argv)
    ui = DVSstartUpPage()
    app.exec_()