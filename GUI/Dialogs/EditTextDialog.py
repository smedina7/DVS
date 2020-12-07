from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QPushButton, QMessageBox, QSizePolicy, QLabel, QPlainTextEdit

class EditTextDialog(QtWidgets.QWidget):
    #Signal for when the user is done editing text
    edited = QtCore.pyqtSignal(str)

    def __init__(self, text_to_edit,):
        QtWidgets.QWidget.__init__(self, parent=None)

        self.edit_text = text_to_edit
        self.new_text = text_to_edit

        #Title of window
        self.outerVertBox = QtWidgets.QVBoxLayout()
        self.outerVertBox.setObjectName("outerVertBox")
        self.setWindowTitle("Edit Text")
        self.setObjectName("EditTextDialog")

        #Edit text area
        self.edit_labelH = QtWidgets.QHBoxLayout()
        self.edit_labelH.setObjectName("editlabellayout")
        self.edit_label = QtWidgets.QLabel("Edit Text:")
        self.edit_label.setObjectName("editLabel")
        self.edit_labelH.addWidget(self.edit_label)

        self.edit_area = QtWidgets.QHBoxLayout()
        self.edit_area.setObjectName("editareahorlayout")
        self.edit_space = QPlainTextEdit()
        self.edit_space.setPlainText(self.edit_text)
        self.edit_space.setFixedHeight(100)
        self.edit_area.addWidget(self.edit_space)

        #Set the button layouts
        self.bottomButtons_layout = QtWidgets.QHBoxLayout()

        #buttons
        self.ok_button = QPushButton("OK")
        self.cancel_button = QPushButton("Cancel")

        self.ok_button.clicked.connect(self.on_ok_clicked)
        self.cancel_button.clicked.connect(self.on_cancel_clicked)

        self.bottomButtons_layout.addWidget(self.ok_button)
        self.bottomButtons_layout.addWidget(self.cancel_button)

        self.outerVertBox.addLayout(self.edit_labelH)
        self.outerVertBox.addLayout(self.edit_area)
        self.outerVertBox.addLayout(self.bottomButtons_layout)

        self.setLayout(self.outerVertBox)

    def on_ok_clicked(self):
        edited_text = self.edit_space.toPlainText()
        if edited_text != self.edit_text:
            self.new_text = edited_text
            self.edited.emit(self.new_text)
            self.close()
        else:
            self.edited.emit(self.new_text)
            self.close()

    def on_cancel_clicked(self, event):
        self.quit_event = event

        cancel = QMessageBox.question(
            self, "Close Edit Text",
            "Are you sure you want to cancel editing text? \n Any change will be discarded",
            QMessageBox.Close | QMessageBox.Cancel)

        if cancel == QMessageBox.Close:
            self.close()

        elif cancel == QMessageBox.Cancel:
            pass



