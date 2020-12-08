from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel, QMessageBox, QComboBox

class SettingsDialog(QtWidgets.QWidget):
    #Signal for when the user is done changing settings
    sync_enabled = QtCore.pyqtSignal(bool)
    sync_config = QtCore.pyqtSignal(int)

    def __init__(self, is_enabled, s_margin):
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

        #margin for sync
        self.syncLabelLayout2 = QtWidgets.QVBoxLayout()
        self.syncLabelLayout2.setObjectName("syncLabelLayout2")
        self.syncLabel2 = QLabel("Set Sync Margin/Threshold")

        self.comboBox = QComboBox()
        self.comboBox.addItem("0")
        self.comboBox.addItem("1")

        self.comboBox.setCurrentText(str(s_margin))

        #buttons
        self.ok_button = QPushButton("OK")
        self.cancel_button = QPushButton("Cancel")

        #add on click events
        self.ok_button.clicked.connect(self.on_ok_clicked)
        self.cancel_button.clicked.connect(self.on_cancel_clicked)
        self.comboBox.activated[str].connect(self.margin_selected)

        #Set the button layouts
        self.bottomButtons_layout = QtWidgets.QHBoxLayout()

        #put everything together
        self.syncLabelLayout.addWidget(self.syncLabel)
        self.syncLabelLayout.addWidget(self.button)
        self.syncLabelLayout2.addWidget(self.syncLabel2)
        self.syncLabelLayout2.addWidget(self.comboBox)
        self.bottomButtons_layout.addWidget(self.ok_button)
        self.bottomButtons_layout.addWidget(self.cancel_button)

        self.outerVertBox.addLayout(self.syncLabelLayout)
        self.outerVertBox.addLayout(self.syncLabelLayout2)
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
    
    def margin_selected(self, margin):
        margin_int = int(margin)
        self.comboBox.setCurrentText(margin)
        self.sync_config.emit(margin_int)

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