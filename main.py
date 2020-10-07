import logging
import sys
from GUI.Widgets.HomeWindow import MainGUI
from src.fileDirectory import FileDirectory
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QMessageBox
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt
#from PyQt5.QtGui.Qcolor
from PyQt5.uic import loadUi




class DVSstartUpPage(QMainWindow):
    def __init__(self):
        super(DVSstartUpPage, self).__init__()
        loadUi('GUI/src/DVSstartUpPage.ui', self)

        #Dark theme
        darkpalette = QPalette()
        darkpalette.setColor(QPalette.Window, QColor(41,44,51))
        darkpalette.setColor(QPalette.WindowText, Qt.white)
        darkpalette.setColor(QPalette.Base, QColor(15,15,15))
        darkpalette.setColor(QPalette.AlternateBase, QColor(41,44,51))
        darkpalette.setColor(QPalette.ToolTipBase, Qt.white)
        darkpalette.setColor(QPalette.ToolTipText, Qt.white)
        darkpalette.setColor(QPalette.Text, Qt.white)
        darkpalette.setColor(QPalette.Button, QColor(41,44,51))
        darkpalette.setColor(QPalette.ButtonText, Qt.white)
        darkpalette.setColor(QPalette.BrightText, Qt.red)
        darkpalette.setColor(QPalette.Highlight, QColor(100,100,225))
        darkpalette.setColor(QPalette.HighlightedText, Qt.black)
        app.setPalette(darkpalette)

        self.setFixedSize(620,565)
        self.setGeometry(500, 300, 500, 100)
        self.CreateNew_pushButton = self.findChild(QPushButton, 'CreateNew_pushButton')
        self.CreateNew_pushButton.clicked.connect(self.openMain)
        self.CurrentProject_PushButton = self.findChild(QPushButton, 'CurrentProject_PushButton')
        self.CurrentProject_PushButton.clicked.connect(self.openDir)
        self.Settings_pushButton = self.findChild(QPushButton, 'Settings_pushButton')
        self.Settings_pushButton.clicked.connect(self.openSettings)
        self.show()

    def openMain(self):
        self.window = MainGUI()
        self.window.setGeometry(500, 300, 500, 100)
        self.window.show()
        self.close()

    def openDir(self):
        self.folder_chosen = str(QFileDialog.getExistingDirectory(self, "Select Directory to Open Project"))

        if self.folder_chosen == "":
            logging.debug("File choose cancelled")
            return

        if len(self.folder_chosen) > 0:
            QMessageBox.critical(self, 'Nonfunctional Button', f'This button does not work yet\n')
            return

        self.window.show()
        self.close()

    def openSettings(self):
        QMessageBox.critical(self, 'Nonfunctional Button', f'This button does not work yet\n')
        
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
