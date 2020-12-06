import json
import sys
import os.path
import pandas as pd    
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QImage, QIcon
from PyQt5.QtCore import QAbstractTableModel, Qt
from PyQt5.QtWidgets import QTableWidget, QAction, QPushButton, QApplication, QTableView, QWidget, QLabel, QHBoxLayout, QVBoxLayout, QTableWidgetItem
from pathlib import Path, PureWindowsPath


class save:
    def save(self, label, Projectpath):

        labelDataline = label
        path= Projectpath
        datalinepath = ""

        if(labelDataline == "keypresses"):
            keys = ["keypresses_id", "content", "className","Tag", "start"]
            datalinepath = "/ParsedLogs/Keypresses.JSON"
            

        if (labelDataline == "systemcalls"):
            keys = ["auditd_id", "content", "className","Tag","start"]
            datalinepath = "/ParsedLogs/SystemCalls.JSON"
           


        nb_row = self.rowCount()
        nb_col = self.columnCount()

        dct = dict()
        multikeys = []
        dct = dict(zip(keys, [""] * len(keys)))
        
        for row in range (nb_row):
            # for col in range(nb_col):
            col = 0
            for j in keys:
                # print(self.item(row, col).text())
                value = self.item(row, col).text()
                dct[j] = value
                col = col + 1

            multikeys.append(dct)
            dct = dict()


        json_object = json.dumps(multikeys, indent=4)
            
        if sys.platform == "linux" or sys.platform == "linux2":
            jsonpath = path + datalinepath
        
        else:
            #fix windows paths
            jsonpath = path + "\\ParsedLogs\\pcomments.json"

        
        with open(jsonpath, 'w') as jsonfile:
            jsonfile.write(json_object)




