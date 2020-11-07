import json
import sys
import os
import pandas as pd    
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QImage, QIcon
from PyQt5.QtCore import QAbstractTableModel, Qt
from PyQt5.QtWidgets import QTableWidget, QAction, QPushButton, QApplication, QTableView, QWidget, QLabel, QHBoxLayout, QVBoxLayout, QTableWidgetItem
 

class Keypresses(QTableWidget):
    def __init__(self, data, *args):
        QTableWidget.__init__(self, *args)
        self.data = data
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        dfdata = data

        keys = ["keypresses_id", "content", "className", "start"]
        labels = keys
        self.setHorizontalHeaderLabels(labels)
        df = pd.read_json (dfdata)
        
        for ind in df.index:
            c = 0
            tableid = str(ind)
            self.insertRow(self.rowCount())
            
            for j in keys:
                it = QtWidgets.QTableWidgetItem()
                if j == "keypresses_id":
                    it.setData(QtCore.Qt.DisplayRole, (tableid))
                else:
                    it.setData(QtCore.Qt.DisplayRole, (df[j][ind]))

                self.setItem(ind, c, it)
                c= c+1



class SystemCalls(QTableWidget):
    def __init__(self, data, *args):
        QTableWidget.__init__(self, *args)
        self.data = data
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        dfdata = data

        keys = ["auditd_id", "content", "className", "start"]
        labels = keys
        self.setHorizontalHeaderLabels(labels)
        df = pd.read_json (dfdata)
        
        for ind in df.index:
            c = 0
            tableid = str(ind)
            self.insertRow(self.rowCount())
            
            for j in keys:
                it = QtWidgets.QTableWidgetItem()
                if j == "auditd_id":
                    it.setData(QtCore.Qt.DisplayRole, (tableid))
                else:
                    it.setData(QtCore.Qt.DisplayRole, (df[j][ind]))

                self.setItem(ind, c, it)
                c= c+1



