import logging
import subprocess
import os
import sys
from GUI.Widgets.HomeWindow import MainGUI
from GUI.PacketView.Manager import PacketManager
from GUI.Dialogs.NewProjectDialog import NewProjectDialog
from GUI.Dialogs.Settings import SettingsDialog
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QMessageBox, QFileDialog
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi
from PyQt5 import QtCore

class DVSstartUpPage(QMainWindow):
    def __init__(self):
        super(DVSstartUpPage, self).__init__()
        loadUi('GUI/src/DVSstartUpPage.ui', self)
        QApplication.setStyle("Fusion")

        # Now use a palette to switch to dark colors:
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(53, 53, 53))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ToolTipBase, Qt.white)
        palette.setColor(QPalette.ToolTipText, Qt.white)
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.BrightText, Qt.red)
        palette.setColor(QPalette.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.Highlight, QColor(70,70,70))
        palette.setColor(QPalette.HighlightedText, Qt.black)
        QApplication.setPalette(palette)

        self.enabled_sync = False
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
        throughput = self.manager.getThroughput()
        self.window = MainGUI(json_files, clicks, timed, throughput, self.manager)
        self.window.setGeometry(500, 300, 500, 100)
        self.window.show()

    #Slot for when the user created the new project, path and configname
    @QtCore.pyqtSlot(str)
    def project_created(self, project_dir):
        self.project_folder = project_dir
        self.openHomeWindow()
        self.hide()

    @QtCore.pyqtSlot(bool)
    def sync_enabled(self, enabled):
        self.enabled_sync = enabled
        print("IN MAIN: Is Sync Enabled? - " + str(self.enabled_sync))
        #self.settings_popup.hide()
        
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
        self.settings_popup = SettingsDialog(self.enabled_sync)
        self.settings_popup.sync_enabled.connect(self.sync_enabled)
        self.settings_popup.show()
        #QMessageBox.critical(self, 'Nonfunctional Button', f'This button does not work yet\n')
    

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Close Window', 'Are you sure you want to quit?', 
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
            self.close()
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

    
    