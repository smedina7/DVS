import logging
import subprocess
import os
import sys
from GUI.Widgets.HomeWindow import MainGUI
from GUI.PacketView.Manager import PacketManager
from GUI.Dialogs.NewProjectDialog import NewProjectDialog
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QMessageBox, QFileDialog
from PyQt5.uic import loadUi
from PyQt5 import QtCore

class DVSstartUpPage(QMainWindow):
    def __init__(self):
        super(DVSstartUpPage, self).__init__()
        loadUi('GUI/src/DVSstartUpPage.ui', self)
        self.project_folder = ''
        self.setFixedSize(620,565)
        self.setGeometry(500, 300, 500, 100)
        self.CreateNew_pushButton = self.findChild(QPushButton, 'CreateNew_pushButton')
        self.CreateNew_pushButton.clicked.connect(self.createNewProject)
        self.CurrentProject_PushButton = self.findChild(QPushButton, 'CurrentProject_PushButton')
        self.CurrentProject_PushButton.clicked.connect(self.openDir)
        self.Settings_pushButton = self.findChild(QPushButton, 'Settings_pushButton')
        self.Settings_pushButton.clicked.connect(self.openSettings)
        self.show()

    def createNewProject(self):
        self.new_project_popup = NewProjectDialog()
        self.new_project_popup.created.connect(self.project_created)
        self.new_project_popup.show()

    def openHomeWindow(self):
        self.manager = PacketManager(self.project_folder)
        json_files = self.manager.getJSON()
        clicks = self.manager.getClicks()
        timed = self.manager.getTimed()
        self.window = MainGUI(json_files, clicks, timed, self.manager)
        self.window.setGeometry(500, 300, 500, 100)
        self.window.show()

    #Slot for when the user created the new project, path and configname
    @QtCore.pyqtSlot(str)
    def project_created(self, project_dir):
        self.project_folder = project_dir
        self.openHomeWindow()
        self.hide()
        
    def openDir(self):
        folder_chosen = str(QFileDialog.getExistingDirectory(self, "Select Directory to Open Project"))

        if folder_chosen == "":
            logging.debug("File choose cancelled")
            return

        if len(folder_chosen) > 0:
            self.project_folder = folder_chosen
            self.openHomeWindow()
            self.hide()

    def openSettings(self):
        QMessageBox.critical(self, 'Nonfunctional Button', f'This button does not work yet\n')
    
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Close Window', 'Are you sure you want to quit?', 
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
            cmd = "python " + os.getcwd() + "/GUI/Dash/shutdown_dash_server.py"
            print(cmd)
            os.system(cmd)
            print("closed")
        else:
            event.ignore()

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

    
    