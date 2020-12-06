import json
import sys
import os.path
import pandas as pd    
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QImage, QIcon
from PyQt5.QtCore import QAbstractTableModel, Qt
from PyQt5.QtWidgets import QTableWidget, QAction, QPushButton, QApplication, QTableView, QWidget, QLabel, QHBoxLayout, QVBoxLayout, QTableWidgetItem
from pathlib import Path, PureWindowsPath

class TextDataline(QTableWidget):
    def __init__(self, data, label, *args):
        QTableWidget.__init__(self, *args)
        self.data = data
        dfdata = data
        label = label
        keys = []
        
        # reloadDataline.addTagColumn(self,data,label)
        df = pd.read_json (dfdata)



        if(label == "keypresses"):
            keys = ["keypresses_id", "content", "className","Tag", "start"]
            ser = pd.Series(df['keypresses_id']) 

        if (label == "systemcalls"):
            keys = ["auditd_id", "content", "className","Tag","start"]
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
                    it.setFlags(QtCore.Qt.ItemIsEnabled)

                elif j == "auditd_id":
                    tableid = int(ser[ind])
                    it.setData(QtCore.Qt.DisplayRole, (tableid))
                    it.setFlags(QtCore.Qt.ItemIsEnabled)

                elif j == "suricata_id":
                    tableid = str(ser[ind])
                    it.setData(QtCore.Qt.DisplayRole, (tableid))
                    it.setFlags(QtCore.Qt.ItemIsEnabled)

                elif j == "packet_id":
                    tableid = str(ser[ind])
                    it.setData(QtCore.Qt.DisplayRole, (tableid))
                    it.setFlags(QtCore.Qt.ItemIsEnabled)

                elif j == "confidence":
                    tableid = str(ser_confidence[ind])
                    if tableid !='No Data':
                        it.setData(QtCore.Qt.DisplayRole, (tableid))

                elif j == "start":
                    it.setData(QtCore.Qt.DisplayRole, (df[j][ind]))
                    # it.setFlags(QtCore.Qt.ItemIsEnabled)

                elif j == "timestamp":
                    tableid = str(ser_timestamp[ind])
                    it.setData(QtCore.Qt.DisplayRole, (tableid))
                    # it.setFlags(QtCore.Qt.ItemIsEnabled)

                else:
                    it.setData(QtCore.Qt.DisplayRole, (df[j][ind]))

                self.setItem(ind, c, it)
                
                c= c+1

        self.resizeColumnsToContents()
        self.resizeRowsToContents()


class reloadDataline:

    def addTagColumn (datajson):
        path = datajson
        datalines = ["keypresses", "systemcalls"]
        datalinepath = ""

        for label in datalines:
            multikeys = []
            if(label == "keypresses"):
                keys = ["keypresses_id", "content", "className", "start"]
                datalinepath = "/ParsedLogs/Keypresses.JSON"

            if (label == "systemcalls"):
                keys = ["auditd_id", "content", "className", "start"]
                datalinepath = "/ParsedLogs/SystemCalls.JSON"

                
            dfdata = path + datalinepath
            # if (label == "suricata"):
            #     keys = ["suricata_id", "suricata_rule_id", "content", "className", "start"]
            dct = dict()
            colInd = 0
            df = pd.read_json (dfdata)
            for i, row in df.iterrows():
                for j in keys:
                    value = row [j]
                    if(colInd == 3):
                        dct["Tag"] = " "

                    dct[j] = value
                    colInd = colInd + 1

                multikeys.append(dct)
                colInd = 0
                dct = dict()

            # print("MultiKEYS")
            # print(multikeys)

            # path= "/home/kali/DVS_branches/DVS_bsalvarez/DVS/ProjectData/t1"

            json_object = json.dumps(multikeys, indent=4)
            
            if sys.platform == "linux" or sys.platform == "linux2":
                jsonpath = path + datalinepath
            
            else:
                #fix windows paths
                jsonpath = path + "\\ParsedLogs\\pcomments.json"

            
            with open(jsonpath, 'w') as jsonfile:
                jsonfile.write(json_object)


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