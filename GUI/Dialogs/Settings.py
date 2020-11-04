from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel, QMessageBox

class SettingsDialog(QtWidgets.QWidget):
    #Signal for when the user is done changing settings
    sync_enabled = QtCore.pyqtSignal(bool)
    sync_config = QtCore.pyqtSignal(int)

    def __init__(self, is_enabled):
        QtWidgets.QWidget.__init__(self, parent=None)

        #Title of window
        self.outerVertBox = QtWidgets.QVBoxLayout()
        self.outerVertBox.setObjectName("outerVertBox")
        self.setWindowTitle("Settings")
        self.setObjectName("SettingsDialog")

        self.syncLabelLayout = QtWidgets.QVBoxLayout()
        self.syncLabelLayout.setObjectName("syncLabelLayout")
        self.syncLabel = QLabel("Sync On/Off")
        
        #button to turn on or off
        self.button = QPushButton()
        if is_enabled == False:
            self.button.setText("OFF")
            self.button.setStyleSheet("background-color : grey")
        else:
            self.button.setText("ON")
            self.button.setStyleSheet("background-color : blue") 
            
        self.button.setCheckable(True)
        self.button.clicked.connect(self.sync_button_clicked)

        #buttons
        self.ok_button = QPushButton("OK")
        self.cancel_button = QPushButton("Cancel")

        #add on click events
        self.ok_button.clicked.connect(self.on_ok_clicked)
        self.cancel_button.clicked.connect(self.on_cancel_clicked)

        #Set the button layouts
        self.bottomButtons_layout = QtWidgets.QHBoxLayout()

        #put everything together
        self.syncLabelLayout.addWidget(self.syncLabel)
        self.syncLabelLayout.addWidget(self.button)
        self.bottomButtons_layout.addWidget(self.ok_button)
        self.bottomButtons_layout.addWidget(self.cancel_button)

        self.outerVertBox.addLayout(self.syncLabelLayout)
        self.outerVertBox.addLayout(self.bottomButtons_layout)
        self.setLayout(self.outerVertBox)

    def sync_button_clicked(self):
        if self.button.text() == "OFF":
            self.button.setStyleSheet("background-color : blue") 
            self.button.setText("ON")
            self.sync_enabled.emit(True)
        else:
            self.button.setStyleSheet("background-color : grey")
            self.button.setText("OFF")
            self.sync_enabled.emit(False)

    def on_cancel_clicked(self, event):
        self.quit_event = event

        cancel = QMessageBox.question(
            self, "Close New Project",
            "Are you sure you want to cancel changing settings?",
            QMessageBox.Close | QMessageBox.Cancel)

        if cancel == QMessageBox.Close:
            self.close()

        elif cancel == QMessageBox.Cancel:
            pass

    def on_ok_clicked(self):
        self.close()