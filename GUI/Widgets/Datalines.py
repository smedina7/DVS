import json
import sys
import os
import pandas as pd    
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QImage, QIcon
from PyQt5.QtCore import QAbstractTableModel, Qt
from PyQt5.QtWidgets import QPushButton, QApplication, QTableView, QWidget, QLabel, QHBoxLayout

class Datalines(QtWidgets.QWidget):
    def __init__(self, data, dataline_type):
        QtWidgets.QWidget.__init__(self, parent=None)

        #json data
        self._data = data
        dfdata = data

        #dataline chosen
        self.dl_type = dataline_type

    def createKeypresses(self):
        return
    
    def createMouseclicks(self):
        return

    def createTimedScreenshots(self):
        return
    
    def createThroughput(self):
        return

    def createOther(self):
        return


