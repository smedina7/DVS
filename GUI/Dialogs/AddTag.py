from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QPushButton, QMessageBox, QSizePolicy, QLabel, QPlainTextEdit

class AddTagDialog(QtWidgets.QWidget):
    #Signal for when the user is done adding tag
    added = QtCore.pyqtSignal(str)

    def __init__(self, text_to_add):
        QtWidgets.QWidget.__init__(self, parent=None)

        self.add_text = text_to_add
        self.new_text = text_to_add

        #Title of window
        self.outerVertBox = QtWidgets.QVBoxLayout()
        self.outerVertBox.setObjectName("outerVertBox")
        self.setWindowTitle("Add Tag")
        self.setObjectName("AddTagDialog")

        #add text area
        self.add_labelH = QtWidgets.QHBoxLayout()
        self.add_labelH.setObjectName("addlabellayout")
        self.add_label = QtWidgets.QLabel("Add Tag:")
        self.add_label.setObjectName("AddLabel")
        self.add_labelH.addWidget(self.add_label)

        self.add_area = QtWidgets.QHBoxLayout()
        self.add_area.setObjectName("addareahorlayout")
        self.add_space = QPlainTextEdit()
        self.add_space.setPlainText(self.add_text)
        self.add_space.setFixedHeight(100)
        self.add_area.addWidget(self.add_space)

        #Set the button layouts
        self.bottomButtons_layout = QtWidgets.QHBoxLayout()

        #buttons
        self.ok_button = QPushButton("OK")
        self.cancel_button = QPushButton("Cancel")

        self.ok_button.clicked.connect(self.on_ok_clicked)
        self.cancel_button.clicked.connect(self.on_cancel_clicked)

        self.bottomButtons_layout.addWidget(self.ok_button)
        self.bottomButtons_layout.addWidget(self.cancel_button)

        self.outerVertBox.addLayout(self.add_labelH)
        self.outerVertBox.addLayout(self.add_area)
        self.outerVertBox.addLayout(self.bottomButtons_layout)

        self.setLayout(self.outerVertBox)

    def on_ok_clicked(self):
        added_text = self.add_space.toPlainText()
        if added_text != self.add_text:
            self.new_text = added_text
            self.added.emit(self.new_text)
            self.close()
        else:
            self.added.emit(self.new_text)
            self.close()

    def on_cancel_clicked(self, event):
        self.quit_event = event

        cancel = QMessageBox.question(
            self, "Close Add Tag",
            "Are you sure you want to cancel adding tag? \n Any change will be discarded",
            QMessageBox.Close | QMessageBox.Cancel)

        if cancel == QMessageBox.Close:
            self.close()

        elif cancel == QMessageBox.Cancel:
            pass