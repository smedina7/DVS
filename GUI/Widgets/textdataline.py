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

        df = pd.read_json (dfdata)

        if(label == "keypresses"):
            keys = ["keypresses_id", "content", "className", "start"]
            ser = pd.Series(df['keypresses_id']) 

        if (label == "systemcalls"):
            keys = ["auditd_id", "content", "className", "start"]
            ser = pd.Series(df['auditd_id']) 

        if (label == "suricata"):
            keys = ["suricata_id", "suricata_rule_id", "content", "className", "start"]
            ser = pd.Series(df['suricata_id']) 
        
        if (label == "packetcomments"):
            keys = ["packet_id", "scope", "important-packet-identifier","program-used", "cmd", "description", "confidence","timestamp" ]
            ser = pd.Series(df['packet_id']) 
            ser_confidence = pd.Series(df['confidence']) 
            ser_timestamp = pd.Series(df['timestamp']) 
            
        labels = keys
        self.setHorizontalHeaderLabels(labels)
        
        for ind in df.index:
            c = 0
            # tableid = str(ind)
            self.insertRow(self.rowCount())
            
            for j in keys:
                it = QtWidgets.QTableWidgetItem()
                if j == "keypresses_id":
                    tableid = str(ser[ind])
                    it.setData(QtCore.Qt.DisplayRole, (tableid))

                elif j == "auditd_id":
                    tableid = str(ser[ind])
                    it.setData(QtCore.Qt.DisplayRole, (tableid))

                elif j == "suricata_id":
                    tableid = str(ser[ind])
                    it.setData(QtCore.Qt.DisplayRole, (tableid))

                elif j == "packet_id":
                    tableid = str(ser[ind])
                    it.setData(QtCore.Qt.DisplayRole, (tableid))

                elif j == "confidence":
                    tableid = str(ser_confidence[ind])
                    if tableid !='nan':
                        it.setData(QtCore.Qt.DisplayRole, (tableid))

                elif j == "timestamp":
                    tableid = str(ser_timestamp[ind])
                    it.setData(QtCore.Qt.DisplayRole, (tableid))

                else:
                    it.setData(QtCore.Qt.DisplayRole, (df[j][ind]))

                self.setItem(ind, c, it)
                c= c+1

        self.resizeColumnsToContents()
        self.resizeRowsToContents()



class reloadDataline:
    def reloadDataline(self, path, label):   
        # QTableWidget.__init__(self, *args)
        print("LABEL from reload dataline", label)
        currentRowCount = self.rowCount()
        totalcolumns = self.columnCount()
        # print("From reload dataline", currentRowCount, totalcolumns)
        self.clearContents()
        keys = ["packet_id", "scope", "important-packet-identifier","program-used", "cmd", "description", "confidence","timestamp" ]

        dfdata =  path
        df = pd.read_json (dfdata)
        row = 0

        
        for ind in df.index:
            it = QtWidgets.QTableWidgetItem()
            c = 0

            if row == currentRowCount:
                self.insertRow(self.rowCount())
                for j in keys:
                    val = df[j][ind]
                    item = QTableWidgetItem(str(val))
                    self.setItem(ind,c, item)
                    c = c + 1
                    row= row + 1

            else: 
                for j in keys:
                    val = df[j][ind]
                    item = QTableWidgetItem(str(val))
                    self.setItem(ind,c, item)
                    c = c + 1
            
            row = row + 1
          


                
                
                
