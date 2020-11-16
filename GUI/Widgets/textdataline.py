import json
import sys
import os
import pandas as pd    
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QImage, QIcon
from PyQt5.QtCore import QAbstractTableModel, Qt
from PyQt5.QtWidgets import QTableWidget, QAction, QPushButton, QApplication, QTableView, QWidget, QLabel, QHBoxLayout, QVBoxLayout, QTableWidgetItem

class TextDataline(QTableWidget):
    def __init__(self, data, label, *args):
        QTableWidget.__init__(self, *args)
        self.data = data
        dfdata = data
        label = label
        keys = []

        if(label == "keypresses"):
            keys = ["keypresses_id", "content", "className", "start"]

        if (label == "systemcalls"):
            keys = ["auditd_id", "content", "className", "start"]

        if (label == "suricata"):
            keys = ["suricata_id", "suricata_rule_id", "content", "className", "start"]

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
                if j == "auditd_id":
                    it.setData(QtCore.Qt.DisplayRole, (tableid))
                if j == "suricata_id":
                    it.setData(QtCore.Qt.DisplayRole, (tableid))
                else:
                    it.setData(QtCore.Qt.DisplayRole, (df[j][ind]))

                self.setItem(ind, c, it)
                c= c+1

        self.resizeColumnsToContents()
        self.resizeRowsToContents()
