import logging
import sys
import os
from GUI.Widgets.HomeWindow import MainGUI
from PacketView.Manager import PacketManager
from src.fileDirectory import FileDirectory
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QMessageBox, QFileDialog
from PyQt5.uic import loadUi


class DVSstartUpPage(QMainWindow):
    def __init__(self):
        super(DVSstartUpPage, self).__init__()
        loadUi('GUI/src/DVSstartUpPage.ui', self)

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
        self.folder_chosen = str(QFileDialog.getExistingDirectory(self, "Select Project Directory you want to analyze"))

        if self.folder_chosen == "":
            logging.debug("File choose cancelled")
            return

        if len(self.folder_chosen) > 0:
            project_path_chosen = os.path.abspath(self.folder_chosen)
            
        self.manager = PacketManager(project_path_chosen)
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
