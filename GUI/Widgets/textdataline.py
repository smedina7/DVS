import json
import sys
import os
import pandas as pd    
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QImage, QIcon
from PyQt5.QtCore import QAbstractTableModel, Qt
from PyQt5.QtWidgets import QPushButton, QApplication, QTableView, QWidget, QLabel, QHBoxLayout
 
class Keypresses(QtWidgets.QMainWindow):
    def __init__(self, data):
        # super(First, self).__init__(parent)
        QtWidgets.QMainWindow.__init__(self)
        self._data = data
        dfdata = data


        keys = ["keypresses_id", "content", "className", "start"]
        labels = keys
        w = QtWidgets.QTableWidget(0, len(labels))
        w.setHorizontalHeaderLabels(labels)
        df = pd.read_json (dfdata)
        
        for ind in df.index:
            c = 0
            tableid = str(ind)
            w.insertRow(w.rowCount())
            
            for j in keys:
                btn= QtWidgets.QPushButton()
                it = QtWidgets.QTableWidgetItem()
                if j == "keypresses_id":
                    it.setData(QtCore.Qt.DisplayRole, (tableid))
                else:
                    it.setData(QtCore.Qt.DisplayRole, (df[j][ind]))

                w.setItem(ind, c, it)
                c= c+1

        self.setCentralWidget(w)

class SystemCalls(QtWidgets.QMainWindow):
    def __init__(self, data):
        # super(First, self).__init__(parent)
        QtWidgets.QMainWindow.__init__(self)
        self._data = data
        dfdata = data


        keys = ["auditd_id", "content", "className", "start"]
        labels = keys
        w = QtWidgets.QTableWidget(0, len(labels))
        w.setHorizontalHeaderLabels(labels)
        df = pd.read_json (dfdata)
        
        for ind in df.index:
            c = 0
            tableid = str(ind)
            w.insertRow(w.rowCount())
            
            for j in keys:
                btn= QtWidgets.QPushButton()
                it = QtWidgets.QTableWidgetItem()
                if j == "auditd_id":
                    it.setData(QtCore.Qt.DisplayRole, (tableid))
                else:
                    it.setData(QtCore.Qt.DisplayRole, (df[j][ind]))

                w.setItem(ind, c, it)
                c= c+1

        self.setCentralWidget(w)