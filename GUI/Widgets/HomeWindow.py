import logging

from PyQt5 import QtGui
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget

class MainGUI(QMainWindow):
    def __init__(self):
        logging.debug("MainGUI(): Instantiated")
        super(MainGUI, self).__init__()
        self.setWindowTitle("Timeline View")
        self.setFixedSize(670,565)

        self.mainWidget = QWidget()
        mainlayout = QVBoxLayout()

        self.mainWidget.setLayout(mainlayout)


